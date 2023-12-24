from fastapi import FastAPI, Depends

from src.auth.base_config import auth_backend, fastapi_users, current_active_user
from src.auth.models import User
from src.auth.schemas import UserRead, UserCreate, UserUpdate

from src.python_questions.routes import router as python_router
from src.python_questions.database import initiate_database


app = FastAPI(title="InterviewApp")

#@app.on_event("startup")
#async def start_db():
 #   await initiate_database()

app.include_router(fastapi_users.get_auth_router(auth_backend),
                   prefix="/auth/bearer",
                   tags=["Authentication"])

app.include_router(fastapi_users.get_register_router(UserRead, UserCreate),
                   prefix="/register",
                   tags=["Authentication"])


app.include_router(python_router, tags=["python questions"], prefix="/python_questions")




