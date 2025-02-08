from sqlalchemy.ext.asyncio import AsyncSession

from core import logger
from users.database.repositories.user import UserRepository
from users.schemas.sign_up import SignUpSchema
from users.utils.cookie import put_token_in_cookies
from fastapi import Response


async def create_user(
    session: AsyncSession,
    credentials: SignUpSchema,
    response: Response,
) -> None:
    user_id = await UserRepository.create_object(
        session=session, data=credentials.model_dump()
    )
    put_token_in_cookies(
        user_id=user_id, response=response, username=credentials.username
    )
    logger.warning(
        "Зарегистрирован новый пользователь",
        extra={"user_id": user_id, "username": credentials.username},
    )
