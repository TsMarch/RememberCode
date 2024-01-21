import uuid
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    nickname: str
    email: EmailStr
    hashed_password: str
    user_level: str
