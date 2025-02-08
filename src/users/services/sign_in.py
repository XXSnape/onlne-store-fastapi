from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from core import logger
from users.database.repositories.user import UserRepository
from users.exceptions.auth import unauthorized_error
from users.schemas.sign_in import SignInSchema
from users.utils.auth import validate_password
from users.utils.cookie import put_token_in_cookies


async def login_user(
    session: AsyncSession, credentials: SignInSchema, response: Response
) -> None:
    user = await UserRepository.get_object_attrs_by_params(
        "id",
        "password",
        "is_admin",
        session=session,
        data={"username": credentials.username},
    )
    if (
        user is None
        or validate_password(
            password=credentials.password, hashed_password=user.password
        )
        is False
    ):
        logger.info(
            "Не удалось авторизоваться",
            extra={"username": credentials.username},
        )
        raise unauthorized_error
    put_token_in_cookies(
        user_id=user.id,
        response=response,
        username=credentials.username,
        is_admin=user.is_admin,
    )
