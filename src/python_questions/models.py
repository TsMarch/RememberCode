from typing import Optional, List

from pydantic import ConfigDict, BaseModel, Field


class QuestionModel(BaseModel):
    """
    Модель для списка вопросов
    """
    id: int = Field(alias="_id")
    question: str = Field(...)
    answer: str = Field(...)


