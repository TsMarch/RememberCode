import pprint

import motor.motor_asyncio
from pydantic import BaseModel
from pymongo import ReturnDocument
from bson import ObjectId
from src.config import DB_PORT_MONGO, DB_HOST

client = motor.motor_asyncio.AsyncIOMotorClient(f"mongodb://{DB_HOST}:{DB_PORT_MONGO}")

database = client["appDB"]
question_collection = database["series"]


# async def do_find():
  #  async for document in question_collection.find({}):
   #     pprint.pprint(document)


# loop = client.get_io_loop()

# loop.run_until_complete(do_find())

print(question_collection.find().to_list(1000))
