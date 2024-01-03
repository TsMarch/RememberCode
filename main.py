from fastapi import FastAPI, Depends

from src.auth.base_config import auth_backend, fastapi_users, current_active_user
from src.auth.models import User
from src.auth.schemas import UserRead, UserCreate
from src.python_questions.models import Question

from src.python_questions.routes import router as python_router
from src.python_questions.database import initiate_database
app = FastAPI(title="InterviewApp")


# MongoDB startup connection
@app.on_event("startup")
async def start_db():
    await initiate_database()
    test = Question(_id="1", question="1", answer="1")
    await test.insert()


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}

# Authentication router
app.include_router(fastapi_users.get_auth_router(auth_backend),
                   prefix="/auth",
                   tags=["Authentication"])

# Register router
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate),
                   prefix="/register",
                   tags=["Authentication"])

# Router for retrieving questions from mongodb
app.include_router(python_router, tags=["python questions"], prefix="/python_questions")


