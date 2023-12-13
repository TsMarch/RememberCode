from pymongo import MongoClient
from bson.json_util import loads, dumps
from src.config import DB_HOST, DB_PORT_MONGO

from fastapi import APIRouter, Request

client = MongoClient(DB_HOST, int(DB_PORT_MONGO))

router = APIRouter()


@router.get("/all_questions", response_description="List of all python questions")
async def list_python_questions(request: Request):
    questions = request.app.database["series"].find()
    final = dumps(questions)
    return loads(final)
