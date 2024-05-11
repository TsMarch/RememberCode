from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.database import get_async_session
from api.python_questions.questions_utils import get_all_questions
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/", response_description="Questions retrieved")
async def get_questions(session: AsyncSession = Depends(get_async_session)):
    questions = await get_all_questions(session)
    return questions

