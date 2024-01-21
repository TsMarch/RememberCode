from fastapi import FastAPI, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from api.auth import utils
from api.database import get_async_session
from api.python_questions.routes import router as python_router
from api.python_questions.database import initiate_database
from api.auth.auth_config import router as register_router
from api.auth.schemas import User


app = FastAPI(title="InterviewApp")

@app.post("/registr/")
async def add_user(user: User, session: AsyncSession = Depends(get_async_session)):
    user = await utils.add_user(session, user.nickname, user.email, user.hashed_password)
    try:
        await session.commit()
        return user
    except IntegrityError as ex:
        await session.rollback()
        raise IntegrityError("This user already exists")


# PostgreSQl test connection
@app.get("/check_connection", response_model=list[User])
async def get_connection_status(session: AsyncSession = Depends(get_async_session)):
    check = await utils.get_conn(session)
    return check


# MongoDB startup connection
#@app.on_event("startup")
#async def start_db():
 #   await initiate_database()
  #  test = Question(_id="1", question="1", answer="1")
   # await test.insert()

# Authentication router
app.include_router(register_router, tags=["Auth status router"])

# Router for retrieving questions from mongodb
app.include_router(python_router, tags=["Python questions"], prefix="/python_questions")


