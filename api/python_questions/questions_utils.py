from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.python_questions.models import Questions


async def get_all_questions(session: AsyncSession):
    query = await session.execute(select(Questions))
    result = query.scalars().all()
    if result is None:
        raise HTTPException(status_code=400, detail="Not found")
    return result
