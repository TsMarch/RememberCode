from fastapi import FastAPI, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from api.auth import utils
from api.database import get_async_session
from api.python_questions.routes import router as python_router
from api.python_questions.database import initiate_database
from api.auth.auth_config import router as register_router
from api.auth.schemas import User, UserRead


app = FastAPI(title="InterviewApp")


# Registration form
@app.post("/registration/")
async def add_user(user: User, session: AsyncSession = Depends(get_async_session)):
    user = await utils.add_user(session, user.nickname, user.email, user.hashed_password)
    try:
        await session.commit()
        return user
    except IntegrityError as ex:
        await session.rollback()
        raise IntegrityError("This user already exists")


# Get user by nickname
@app.post("/get_user/", response_model=list[User])
async def get_user_by_nickname(user: UserRead, session: AsyncSession = Depends(get_async_session)):
    check = await utils.get_user_by_nickname(session, user.nickname)
    return check


# MongoDB startup connection and test data insertion
#@app.on_event("startup")
#async def start_db():
 #   await initiate_database()
  #  test = Question(_id="1", question="1", answer="1")
   # await test.insert()

# Authentication router
app.include_router(register_router, tags=["Auth status router"])

# Router for retrieving questions from mongodb
app.include_router(python_router, tags=["Python questions"], prefix="/python_questions")


