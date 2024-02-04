import uuid

from sqlalchemy import Boolean, String, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from pydantic import EmailStr


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "reg-users"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True, index=True)
    nickname: Mapped[str] = mapped_column(String(length=20), unique=True, nullable=False)
    email: Mapped[EmailStr] = mapped_column(String(length=320), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    user_level: Mapped[str] = mapped_column(String(length=20), default="Beginner", nullable=False)
    disabled: Mapped[str] = mapped_column(String, default="False", nullable=False)
