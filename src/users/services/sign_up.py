from sqlalchemy.ext.asyncio import AsyncSession

from users.database.repositories.user import UserRepository
from users.utils.cookie import put_token_in_cookies
from users.utils.auth import get_hashed_password
from fastapi import Response


async def create_user(
    session: AsyncSession,
    credentials: dict[str, str | bytes],
    response: Response,
) -> None:
    del credentials["name"]
    credentials["fullname"] = "Неизвестно"
    credentials["password"] = get_hashed_password(credentials["password"])
    user_id = await UserRepository.create_object(
        session=session, data=credentials
    )
    put_token_in_cookies(
        user_id=user_id, response=response, username=credentials["username"]
    )
