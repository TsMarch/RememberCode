import pprint
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import motor.motor_asyncio
from pydantic import BaseModel
from pymongo import ReturnDocument, MongoClient
from bson import ObjectId
from api.python_questions.models import Question
from api.config import DB_PORT_MONGO


question_collection = Question


async def initiate_database():
    client = AsyncIOMotorClient("mongodb://mongodb:27017")
    await init_beanie(
        database=client.appDB, document_models=[Question]
    )


async def retrieve_questions() -> List[Question]:
    questions = await question_collection.all().to_list()
    return questions

# async def initiate_database():
#    client = motor.motor_asyncio.AsyncIOMotorClient(f"mongodb://{DB_HOST}:{DB_PORT_MONGO}")
#    database = client.appdb
#    question_collection = database.get_collection("series")
#    await init_beanie(database=client.get_database("appDB"), document_models=[Question])

