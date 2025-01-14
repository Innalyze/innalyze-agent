from ConfigService import ConfigService

from base import bootstrap
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain_community.chat_message_histories import (
    PostgresChatMessageHistory,
)
bootstrap()


configService = ConfigService()
chat_message_history = PostgresChatMessageHistory(
    session_id="test_session", connection_string=configService.get_database_url()
)
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)

model = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.6
)

prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a friendly AI assistant."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])



history = PostgresChatMessageHistory(
    session_id="test_session", connection_string=configService.get_database_url()
)

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    chat_memory=history,
)

# chain = prompt | model
chain = LLMChain(
    llm=model,
    prompt=prompt,
    verbose=True,
    memory=memory
)



# Prompt 2
q2 = { "input": "what did i ask you ?" }
resp2 = chain.invoke(q2)
print(resp2["text"])