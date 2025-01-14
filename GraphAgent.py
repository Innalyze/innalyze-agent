import json
from decimal import Decimal
from typing import Literal, Annotated, TypedDict

from langchain_core.messages import HumanMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.constants import END
from langgraph.graph import MessagesState, StateGraph, START, add_messages
from langgraph.prebuilt import ToolNode
from psycopg import AsyncConnection
from sqlalchemy import text

from Text2SQL import load_prompt
from base import get_session, config

from models.dto.Question import Question



class ExtendedMessageState(TypedDict):
    messages: Annotated[list, add_messages]
    # You can add additional custom keys
    conversation: str


@tool
def run_sql(
        sql_query: Annotated[str, "A valid Postgres SQL Query."]
) -> str:
    """Runs the given Postgres SQL query and return the requested result"""
    l = []

    def decimal_to_float(obj):
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    with get_session() as session:
        result = session.execute(text(sql_query),
                                 execution_options={"postgresql_cursor_factory": "DictCursor"}).mappings().all()

        l = [dict(row) for row in result]
    return json.dumps(l, default=decimal_to_float)


tools = [run_sql]
tool_node = ToolNode(tools)
model = ChatOpenAI(temperature=0, model="gpt-4o", streaming=True)
bound_model = model.bind_tools(tools)


def should_continue(state: ExtendedMessageState):
    """Return the next node to execute."""
    last_message = state["messages"][-1]
    # If there is no function call, then we finish
    if not last_message.tool_calls:
        return END
    # Otherwise if there is, we continue
    return "action"


def filter_messages(messages: list):
    # This is very simple helper function which only ever uses the last message
    return messages[-1:]


# Define the function that calls the model
# def call_model(state: ExtendedMessageState):
#     # messages = filter_messages(state["messages"])
#     print("print: -----",state["messages"])
#     print(state)
#     messages = state["messages"]
#     conversation = state["conversation"]
#
#     if conversation is None:
#         conversation = ""
#
#     if messages[-1].type == "ai" and messages[-1].tool_calls:
#         response = bound_model.invoke(messages[-3:])
#
#         conversation = conversation + "\nToolCall({t})\nAi({c})".format(c=response.content,t=messages[-1])
#         # We return a list, because this will get added to the existing list
#         return {"messages": response, conversation: conversation}
#
#     message = get_prompt(conversation).invoke({"question": messages[-1].content}).to_string()
#
#
#     conversation = conversation+"\nHuman({c})".format(c=message)
#     messages = [HumanMessage(content=message)]
#     response = bound_model.invoke(messages)
#
#     conversation = conversation + "\nAi({c})".format(c=response.content)
#     # We return a list, because this will get added to the existing list
#     return {"messages": response, conversation:conversation}
def call_model(state: ExtendedMessageState):
    messages = state["messages"]
    conversation = state["conversation"]  # Use .get() with a default
    print(state)

    if messages[-1].type == "tool":
        # print(messages[:-3])
        response = bound_model.invoke(messages[-3:])

        conversation += f"\nToolCall({messages[-1]})\nAi({response.content})"
        return {
            "messages": [response],
            "conversation": conversation
        }

    message = get_prompt(conversation).invoke({"question": messages[-1].content}).to_string()
    print(message)
    print(conversation)
    conversation += f"\nHuman({message})"
    messages = [HumanMessage(content=message)]
    response = bound_model.invoke(messages)

    conversation += f"\nAi({response.content})"
    return {
        "messages": [response],
        "conversation": conversation
    }
def get_prompt(history: str):
    return PromptTemplate(
        template="""
    Please answer the question. Your response should ONLY be based on the given tables and conversation history and follow the response guidelines.

    ===Tables
    {tables}

    ===Response Guidelines

    1. Please use the most relevant table(s).
    2. Don't answer question that are not related to the given tables.
        
    ===Conversation history
    ({history})
    
    ===Question
    {question}

    """,
        input_variables=["question", "tables", "history"],
        partial_variables={"tables": load_prompt(), "history":history},
    )
# Define a new graph
workflow = StateGraph(ExtendedMessageState)

# Define the two nodes we will cycle between
workflow.add_node("agent", call_model)
workflow.add_node("action", tool_node)

# Set the entrypoint as `agent`
# This means that this node is the first one called
workflow.add_edge(START, "agent")

# We now add a conditional edge
workflow.add_conditional_edges(
    # First, we define the start node. We use `agent`.
    # This means these are the edges taken after the `agent` node is called.
    "agent",
    # Next, we pass in the function that will determine which node is called next.
    should_continue,
    # Next, we pass in the pathmap - all the possible nodes this edge could go to
    ["action", END],
)

# We now add a normal edge from `tools` to `agent`.
# This means that after `tools` is called, `agent` node is called next.
workflow.add_edge("action", "agent")

async def get_answer(question: Question):
    async with await AsyncConnection.connect(config.get_database_url(), autocommit=True) as conn:
        memory = AsyncPostgresSaver(conn)
        checkpointer_config = {"configurable": {"thread_id": "23"}}

        app = workflow.compile(checkpointer=memory)
        async for c in app.astream({"messages": [question.question], "conversation":""},
                                   checkpointer_config, stream_mode="messages"):
            #print(c)
            # yield "dfg"
            if len(c) > 0:
                yield c[0].content

