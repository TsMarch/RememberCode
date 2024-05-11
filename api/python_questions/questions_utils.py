from fastapi import HTTPException
from api.python_questions.models import Questions
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def get_all_questions(session: AsyncSession):
    query = await session.execute(select(Questions))
    result = query.scalars().all()
    if result is None:
        raise HTTPException(status_code=400, detail="Not found")
    return result
