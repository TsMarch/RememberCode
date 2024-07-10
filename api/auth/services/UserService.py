from fastapi import Depends
from api.auth.models.UserModel import User
from api.auth.schemas import User as UserSchema

from api.auth.repositories.UserRepository import UserRepository


class UserService:

    userRepository: UserRepository

    def __init__(self, userRepository: UserRepository = Depends()) -> None:
        self.userRepository = userRepository

    async def create(self, user_body: UserSchema) -> User:
        return await self.userRepository.create(
            User(nickname=user_body.nickname, email=user_body.email, hashed_password=user_body.hashed_password)
        )
