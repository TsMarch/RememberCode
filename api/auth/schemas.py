import uuid
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    nickname: str
    email: str
    hashed_password: str
    user_level: str
