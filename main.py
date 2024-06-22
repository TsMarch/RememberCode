from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.auth.models import create_tables as auth_table_creation
from api.auth.routers import router as auth_router
from api.python_questions.models import create_tables as questions_tables_creation
from api.python_questions.parser import parse
from api.python_questions.routers import router as python_router
from api.service.routers import router as service_router
from api.users.routers import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await auth_table_creation()
    await questions_tables_creation()
    parse()
    print("База готова к работе")
    yield


app = FastAPI(lifespan=lifespan, title="RememberCode")

# Registration module (look up swagger docs or api/auth/routers)
app.include_router(auth_router, tags=["Authentication module"])

# Users router
app.include_router(user_router, tags=["User routers"])

# Various service routers
app.include_router(service_router, tags=["Service routers"])

# Router for retrieving questions from mongodb
app.include_router(python_router, tags=["Python questions"], prefix="/python_questions")
