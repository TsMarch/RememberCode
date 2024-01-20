from fastapi import FastAPI


from src.python_questions.routes import router as python_router
from src.python_questions.database import initiate_database
from src.auth.auth_config import router as register_router

app = FastAPI(title="InterviewApp")


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


