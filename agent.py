import asyncio
import uuid
from typing import Literal

from langchain.chains.question_answering.map_reduce_prompt import messages


from base import bootstrap, config
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.prebuilt import create_react_agent
from psycopg import Connection,AsyncConnection



bootstrap()
@tool
def get_user_age(name: str) -> str:
    """Use this tool to find the user's age."""
    # This is a placeholder for the actual implementation
    if "bob" in name.lower():
        return "42 years old"
    return "41 years old"
thread_id = uuid.uuid4()
@tool
def get_weather(city: Literal["nyc", "sf"]):
    """Use this to get weather information."""
    if city == "nyc":
        return "It might be cloudy in nyc"
    elif city == "sf":
        return "It's always sunny in sf"
    else:
        raise AssertionError("Unknown city")

# Tell the AI that our name is Bob, and ask it to use a tool to confirm
# that it's capable of working like an agent.
input_message = HumanMessage(content="hi! I'm bob. What is my age?")


async def funct(config1):

    async with await AsyncConnection.connect(config1.get_database_url(), autocommit=True) as conn:
        memory = AsyncPostgresSaver(conn)
        model = ChatOpenAI(streaming=True)
        app = create_react_agent(
            model,
            tools=[get_user_age, get_weather],
            checkpointer=memory,
        )

        config = {"configurable": {"thread_id": "7"}}
        async for c in app.astream({"messages": [("human", "what did i ask you before ?")]}, config,stream_mode="messages"):
            print(c[0].content)
        # memory.setup()
        # The thread id is a unique key that identifies
        # this particular conversation.
        # We'll just generate a random uuid here.
        # This enables a single application to manage conversations among multiple users.


        # res = app.invoke({"messages": [("human", "what's the weather in sf")]}, config)
        # checkpoint = memory.get(config)
        # print(res)
        # print(checkpoint)

        # async for e in app.astream({"messages": [("human", "what's the weather in sf")]}, config, stream_mode="messages"):
        #     print(e)

asyncio.run(funct(config))
    # async for event in app.astream({"messages": [input_message]}, config, stream_mode="values"):
    #     event["messages"][-1].pretty_print()

    # # Confirm that the chat bot has access to previous conversation
    # # and can respond to the user saying that the user's name is Bob.
    # input_message = HumanMessage(content="do you remember my name?")
    #
    # for event in app.stream({"messages": [input_message]}, config1, stream_mode="values"):
    #     event["messages"][-1].pretty_print()
