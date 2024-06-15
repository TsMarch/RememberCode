from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.databases_helper import db_user_helper
from api.python_questions.questions_utils import get_all_questions

router = APIRouter()


@router.get("/", response_description="Questions retrieved")
async def get_questions(
    session: AsyncSession = Depends(db_user_helper.get_async_session),
):
    questions = await get_all_questions(session)
    return questions
