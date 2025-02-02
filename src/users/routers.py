from typing import Annotated

from fastapi import APIRouter, Body, Response
from fastapi import Depends
from starlette.status import HTTP_200_OK

from core import SessionDep, settings
from core.dependencies.user_by_cookie import get_user_id
from .services.sign_up import create_user

router = APIRouter()


@router.post("/sign-up")
async def sign_up(
    credentials: Annotated[str, Body()],
    session: SessionDep,
):
    response = Response()
    await create_user(
        session=session, credentials=credentials, response=response
    )
    return response


@router.post("/sign-out")
async def sign_out():
    response = Response()
    response.delete_cookie(key=settings.auth_jwt.cookie_key_token)
    return response
