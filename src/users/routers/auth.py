from typing import Annotated, Any

from fastapi import APIRouter
from fastapi.params import Depends
from starlette.responses import Response

from core import SessionDep, settings
from core.dependencies.credentials import CredentialsDep, StringOrModel, B
from users.services.sign_in import login_user
from users.services.sign_up import create_user


router = APIRouter()

s = StringOrModel(B)


@router.post("/sign-up")
async def sign_up(
    credentials: Annotated[Any, Depends(s)],
    # credentials: CredentialsDep,
    session: SessionDep,
):
    print("cred from router", credentials, type(credentials))
    response = Response()
    await create_user(
        session=session, credentials=credentials, response=response
    )
    return response


@router.post("/sign-out")
async def sign_out():
    response = Response()
    response.delete_cookie(key=settings.auth_jwt.cookie_key_token)
    response.delete_cookie(key=settings.app.cookie_key_card)
    return response


@router.post("/sign-in")
async def sign_in(credentials: CredentialsDep, session: SessionDep):
    response = Response()
    await login_user(
        session=session, credentials=credentials, response=response
    )
    return response
