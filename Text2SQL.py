from decimal import Decimal
from typing import Annotated

from langchain.chains.question_answering.map_reduce_prompt import messages
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.prebuilt import create_react_agent
from psycopg import AsyncConnection
from pydantic import BaseModel, Field
import json

from sqlalchemy import text

from base import get_session, config
from models.dto.Question import Question


# Define your desired data structure.
class Query(BaseModel):
    query: str = Field(
        description="A valid SQL query (SELECT ...). Any selected column must explicitly converted to string, float or integer")
    explanation: str = Field(description="An explanation of failing to generate the query.")


@tool
def run_sql(
        sql_query: Annotated[str, "A valid Postgres SQL Query."]
) -> str:
    """Runs the given Postgres SQL query and return the requested result"""
    l = []
    print(sql_query)

    def decimal_to_float(obj):
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    try:
        with get_session() as session:

            result = session.execute(text(sql_query),
                                     execution_options={"postgresql_cursor_factory": "DictCursor"}).mappings().all()

            l = [dict(row) for row in result]
    except Exception as e:
        return json.dumps({"error": str(e.__cause__)})
    return json.dumps(l, default=decimal_to_float)


async def answer_question(question: Question):
    # And a query intented to prompt a language model to populate the data structure.

    model = ChatOpenAI(temperature=0, model="gpt-4o-mini")

    prompt = PromptTemplate(
        template="""
Please answer the question. Your response should ONLY be based on the given context and follow the response guidelines.

===Tables
{tables}

===Response Guidelines
1. Please use the most relevant table(s).
2. Don't answer question that are not related to the given tables.
3. Answer using the data from the tables no need for extra info like what are you trying to do don't think out loud. Answer the question straightly.
4. Be creative don't forget that you can use joins or advanced SQL select to fetch the requirement
===Question
{question}

""",
        input_variables=["question", "tables"],
        partial_variables={"tables": load_prompt()},
    )
    model = model.bind_tools([run_sql])
    # chain = prompt | model
    # print(prompt.invoke({"question": question.question}).to_string())
    messages = [HumanMessage(prompt.invoke({"question": question}).to_string())]
    # messages = [prompt.invoke({"question": question}).to_messages()]

    ai_msg = model.invoke(messages)

    messages.append(ai_msg)
    for tool_call in ai_msg.tool_calls:
        selected_tool = {"run_sql": run_sql}[tool_call["name"].lower()]
        print("selected_tool")
        tool_output = selected_tool.invoke(tool_call["args"])
        print(tool_output)
        messages.append(ToolMessage(tool_output, tool_call_id=tool_call["id"]))
    async for c in model.astream(messages):
        yield {"answer": c.content}


async def answer_question_graph(question: Question):
    # And a query intented to prompt a language model to populate the data structure.

    prompt = PromptTemplate(
        template="""
Please answer the question. Your response should ONLY be based on the given context and follow the response guidelines.

===Tables
{tables}

===Response Guidelines

1. Please use the most relevant table(s).
2. Don't answer question that are not related to the given tables.

===Question
{question}

""",
        input_variables=["question", "tables"],
        partial_variables={"tables": load_prompt()},
    )

    async with await AsyncConnection.connect(config.get_database_url(), autocommit=True) as conn:
        memory = AsyncPostgresSaver(conn)
        checkpointer_config = {"configurable": {"thread_id": "8"}}
        model = ChatOpenAI(temperature=0, model="gpt-4o-mini", streaming=True)
        app = create_react_agent(
            model,
            tools=[run_sql],
            checkpointer=memory,
        )

        async for c in app.astream(
                {"messages": [("human", prompt.invoke({"question": question.question}).to_string())]},
                checkpointer_config, stream_mode="messages"):

            yield c[0].content


def text_2_sql2(question):
    # And a query intented to prompt a language model to populate the data structure.

    model = ChatOpenAI(temperature=0, model="gpt-4o-mini")

    parser = JsonOutputParser(pydantic_object=Query)

    prompt = PromptTemplate(
        template="""
You are a {dialect} expert.

Please help to generate a {dialect} query to answer the question. Your response should ONLY be based on the given context and follow the response guidelines and format instructions.

===Tables
{tables}

===Response Guidelines
1. If the provided context is sufficient, please generate a valid query without any explanations for the question. The query should start with a comment containing the question being asked.
2. If the provided context is insufficient, please explain why it can't be generated.
3. Please use the most relevant table(s).
5. Please format the query before responding.
6. Please always respond with a valid well-formed JSON object with the following format

===Response Format
{format_instructions}

===Question
{question}

""",
        input_variables=["dialect", "question", "tables"],
        partial_variables={"format_instructions": parser.get_format_instructions(), "tables": load_prompt(),
                           "dialect": "Postgres"},
    )

    chain = prompt | model | parser

    return chain.invoke({"question": question})


def load_prompt():
    return """

CREATE TABLE reservation_metrics (
    date TIMESTAMP NOT NULL,
    taux_d_occupation_percent DECIMAL(5, 2),
    chambres_disponibles INT,
    chambres_reservees INT,
    duree_du_sejour_jours INT,
    segment_de_clientele VARCHAR(50),  --Type of segments are limited to(Enum):  Leisure,Couples,Business,Group
    source_de_reservation VARCHAR(50)
);


CREATE TABLE revenue_metrics (
    date TIMESTAMP NOT NULL,
    tarif_moyen_journalier_adr_da DECIMAL(10, 2),
    revenu_par_chambre_disponible_revpar_da DECIMAL(10, 2),
    revenu_total_da DECIMAL(15, 2),
    revenu_des_chambres_da DECIMAL(15, 2),
    revenu_annexe_da DECIMAL(15, 2),
    type_de_chambre VARCHAR(50),
    source_de_reservation VARCHAR(50)
);


CREATE TABLE hotel_metrics (
    date TIMESTAMP NOT NULL,
    tarif_moyen_journalier_adr_da DECIMAL(10, 2),
    revenu_par_chambre_disponible_revpar_da DECIMAL(10, 2),
    taux_d_amelioration_percent DECIMAL(5, 2),
    taux_d_annulation_percent DECIMAL(5, 2),
    taux_d_occupation_percent DECIMAL(5, 2),
    duree_moyenne_du_sejour_jours DECIMAL(5, 2),
    segment_de_clientele VARCHAR(50), --Type of segments are limited to(Enum):  Leisure,Couples,Business,Group
    revenu_simple_da DECIMAL(10, 2),
    revenu_double_da DECIMAL(10, 2),
    revenu_suite_da DECIMAL(10, 2),
    revenu_familiale_da DECIMAL(10, 2),
    chambres_disponibles_simple INT,
    chambres_disponibles_double INT,
    chambres_disponibles_suite INT,
    chambres_disponibles_familiale INT
);
    """
