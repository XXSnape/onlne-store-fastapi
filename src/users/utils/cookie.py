from fastapi import Response

from core import settings
from core.utils.jwt import get_access_token


def put_token_in_cookies(
    user_id: int, username: str, is_admin, response: Response
):
    access_token = get_access_token(
        user_id=user_id, username=username, is_admin=is_admin
    )
    response.set_cookie(
        key=settings.auth_jwt.cookie_key_token,
        value=access_token,
        httponly=True,
    )
