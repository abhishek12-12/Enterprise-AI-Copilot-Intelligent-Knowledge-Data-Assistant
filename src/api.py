from src.utils.logger import get_logger
from fastapi import FastAPI
from pydantic import BaseModel

from src.agents.agent import ask_agent


app = FastAPI(
    title="Enterprise AI Copilot API",
    description="REST API for the Enterprise AI Copilot",
    version="1.0.0"
)

logger=get_logger(__name__)
class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {
        "message": "Enterprise AI Copilot API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/ask")
def ask(request: QuestionRequest):
    logger.info(f"Received question: {request.question}")

    answer = ask_agent(request.question)

    logger.info("Question processed successfully")

    return {
        "question": request.question,
        "answer": answer
    }