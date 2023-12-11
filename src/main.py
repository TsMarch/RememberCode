from fastapi import FastAPI, Depends
from pymongo import MongoClient

from src.auth.base_config import auth_backend
from src.auth.manager import get_user_manager
from src.auth.schemas import UserRead, UserCreate
from src.questions.routes import router
from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from src.config import DB_HOST, DB_PORT_MONGO
from src.auth.models import User


client = MongoClient(DB_HOST, int(DB_PORT_MONGO))
app = FastAPI()


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


app.include_router(router, tags=["questions"], prefix="/question")

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)


app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


current_user = fastapi_users.current_user()

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.nickname}"


@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anon"
# async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
  #   return {"q": q, "skip": skip, "limit": limit}


# @app.get("/items/")
# async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
  #  return commons

