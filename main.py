from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends

from api.auth.models import create_tables
from api.python_questions.routers import router as python_router
from api.python_questions.database import initiate_database
from api.auth.security import router as register_router

from api.auth.routers import router as auth_router
from api.users.routers import router as user_router
from api.service.routers import router as service_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("База готова к работе")
    yield

app = FastAPI(lifespan=lifespan, title="RememberCode")

# Registration module (look up swagger docs or api/auth/routers)
app.include_router(auth_router, tags=["Authentication module"])

# Users router
app.include_router(user_router, tags=["User routers"])

# Various service routers
app.include_router(service_router, tags=["Service routers"])




# MongoDB startup connection and test data insertion
#@app.on_event("startup")
#async def start_db():
 #   await initiate_database()
  #  test = Question(_id="1", question="1", answer="1")
   # await test.insert()


# Router for retrieving questions from mongodb
app.include_router(python_router, tags=["Python questions"], prefix="/python_questions")


