from typing import Optional, List

from pydantic import ConfigDict, BaseModel, Field
from beanie import Document


class Question(Document):
    """
    Модель для списка вопросов
    """
    id: int = Field(alias="_id")
    question: str = Field(...)
    answer: str = Field(...)

    class Settings:
        name = "series"

