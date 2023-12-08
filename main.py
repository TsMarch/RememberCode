from fastapi import FastAPI
from pymongo import MongoClient
from routes.routes import router
from config import DB_HOST, DB_PORT_MONGO


client = MongoClient(DB_HOST, int(DB_PORT_MONGO))
app = FastAPI()


# async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
  #   return {"q": q, "skip": skip, "limit": limit}


# @app.get("/items/")
# async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
  #  return commons

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = client
    app.database = app.mongodb_client["appDB"]
    series_collection = app.database["series"]


@app.on_event("shutdown")
def shutdown_db_client():
    client.close()


app.include_router(router, tags=["questions"], prefix="/question")