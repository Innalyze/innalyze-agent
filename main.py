from fastapi import FastAPI
from sqlalchemy import text
from starlette.websockets import WebSocket

from base import get_session
from base import bootstrap
from Text2SQL import answer_question

from models.dto.Question import Question
from starlette.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
import os

bootstrap()
# from GraphAgent import get_answer
app = FastAPI()
api_app = FastAPI(
    openapi_url=None,
    docs_url=None,  # Disable docs (Swagger UI)
    redoc_url=None,  # Disable redoc
)


@api_app.websocket("/ask")
async def answer(socket: WebSocket):
    await socket.accept()
    question: Question = Question.model_validate_json(await socket.receive_text())
    async for an in answer_question(question):
        await socket.send_text(str(an))
    await socket.close()


app.mount("/api", api_app)

if os.path.exists(os.path.join("front", "dist", 'index.html')):
    app.mount(path="/",
              app=StaticFiles(directory="front/dist", html=True),
              name="front")
