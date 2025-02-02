from sqlalchemy.ext.asyncio import AsyncSession
from json import loads

from users.database.repositories.user import UserRepository
from users.services.utils.cookie import put_token_in_cookies
from users.utils.auth import get_hashed_password
from fastapi import Response


async def create_user(
    session: AsyncSession, credentials: str, response: Response
) -> None:
    user_data = loads(credentials)
    del user_data["name"]
    user_data["fullname"] = "Неизвестно"
    user_data["password"] = get_hashed_password(user_data["password"])
    user_id = await UserRepository.create_object(
        session=session, data=user_data
    )
    put_token_in_cookies(
        user_id=user_id, response=response, username=user_data["username"]
    )
