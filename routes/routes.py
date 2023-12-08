from fastapi import APIRouter, Request
from bson.json_util import loads, dumps


router = APIRouter()


@router.get("/question", response_description="List all questions")
def list_questions(request: Request):
    questions = request.app.database["series"].find()
    final = dumps(questions)
    return loads(final)
