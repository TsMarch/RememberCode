from fastapi_users import schemas
from fastapi_users.schemas import PYDANTIC_V2


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    nickname: str
    user_level: str

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    email: str
    password: str
    nickname: str
    user_level: str



