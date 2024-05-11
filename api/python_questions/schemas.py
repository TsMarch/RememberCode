from pydantic import BaseModel


class Questions(BaseModel):
    index: int
    question: str
    answer: str
