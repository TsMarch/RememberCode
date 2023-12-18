from fastapi_users import schemas
from pydantic import EmailStr

class UserRead(schemas.BaseUser[int]):

    id: int
    email: EmailStr
    nickname: str
    user_level: str

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    password: str
    nickname: str
    user_level: str


class UserUpdate(schemas.BaseUserUpdate):
    password: str
    email: EmailStr
    is_active: str
    is_superuser: str
    is_verified: str


