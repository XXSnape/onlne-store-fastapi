from json import loads

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from users.database.repositories.user import UserRepository
from users.exceptions.auth import unauthorized_error
from users.services.utils.cookie import put_token_in_cookies
from users.utils.auth import validate_password


async def login_user(
    session: AsyncSession, credentials: str, response: Response
) -> None:
    user_data = loads(credentials)
    user = await UserRepository.get_object_attrs_by_params(
        "id",
        "password",
        session=session,
        data={"username": user_data["username"]},
    )
    if (
        user is None
        or validate_password(
            password=user_data["password"], hashed_password=user[1]
        )
        is False
    ):
        raise unauthorized_error
    put_token_in_cookies(
        user_id=user[0], response=response, username=user_data["username"]
    )
