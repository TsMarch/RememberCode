from pymongo import MongoClient
from bson.json_util import loads, dumps
from src.config import DB_HOST, DB_PORT_MONGO
from src.python_questions.models import Question
from src.python_questions.database import retrieve_questions
from fastapi import APIRouter, Request, Body


router = APIRouter()


@router.get("/", response_description="Questions retrieved")
async def get_questions():
    questions = await retrieve_questions()
    return questions

