from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.configs.database import db_user_helper
from api.auth.models import UserModel


class UserRepository:
    db: AsyncSession

    def __init__(self, db: AsyncSession = Depends(db_user_helper.connection)) -> None:
        self.db = db

    async def create(self, user: UserModel):
        self.db.add(user)
        await self.db.flush()
        await self.db.commit()
        return user
