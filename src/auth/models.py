from sqlalchemy import Boolean, String, Integer, ForeignKey

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from pydantic import EmailStr

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyBaseUserTableUUID


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    nickname: Mapped[str] = mapped_column(String(length=20), unique=True, nullable=False)
    email: Mapped[EmailStr] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    user_level: Mapped[str] = mapped_column(String(length=20), default="Beginner", nullable=False)

