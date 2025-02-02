from sqlalchemy.ext.asyncio import AsyncSession
from json import loads

from users.database.repositories.user import UserRepository
from users.utils.auth import get_hashed_password


async def create_user(session: AsyncSession, credentials: str):
    user_data = loads(credentials)
    del user_data["name"]
    user_data["fullname"] = "Неизвестно"
    user_data["password"] = get_hashed_password(user_data["password"])
    await UserRepository.create_object(session=session, data=user_data)
