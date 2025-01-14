from fastapi import FastAPI
from sqlalchemy import text
from starlette.websockets import WebSocket

from base import get_session
from base import bootstrap
from Text2SQL import answer_question

from models.dto.Question import Question
from starlette.responses import StreamingResponse
bootstrap()
# from GraphAgent import get_answer
app = FastAPI()





@app.websocket("/api/ask")
async def answer(socket:WebSocket):
    await socket.accept()
    question: Question = Question.model_validate_json(await socket.receive_text())
    async for an in answer_question(question):
        await socket.send_text(str(an))
    await socket.close()

# @app.post("/ask1")
# async def answer1(question: Question ):
#     return answer_question(question)


