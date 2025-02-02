from typing import Annotated, TypeAlias

from fastapi import APIRouter, Body
from fastapi import Depends
from starlette.responses import Response
from starlette.status import HTTP_200_OK

from core import SessionDep, settings
from core.dependencies.user_by_cookie import get_user_id
from .schemas.sign_in import SignInSchema
from .services.sign_in import login_user
from .services.sign_up import create_user

router = APIRouter()

Credentials: TypeAlias = Annotated[str, Body()]


@router.post("/sign-up")
async def sign_up(
    credentials: Credentials,
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


@router.post("/sign-in")
async def sign_in(credentials: Credentials, session: SessionDep):
    response = Response()
    await login_user(
        session=session, credentials=credentials, response=response
    )
    return response
