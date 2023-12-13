from fastapi import FastAPI

from src.auth.base_config import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate

from src.python_questions.routes import router as python_router
from src.python_questions.routes import client

app = FastAPI(title="InterviewApp")


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = client
    app.database = app.mongodb_client["appDB"]
    series_collection = app.database["series"]


app.include_router(fastapi_users.get_auth_router(auth_backend),
                   prefix="/auth/jwt",
                   tags=["Authentication"])

app.include_router(fastapi_users.get_register_router(UserRead, UserCreate),
                   prefix="/register",
                   tags=["Authentication"])

app.include_router(python_router, tags=["python questions"], prefix="/python_questions")
