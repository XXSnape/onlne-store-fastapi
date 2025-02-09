from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from starlette.responses import Response

from core import SessionDep, settings
from core.dependencies.body import SchemaDep
from users.schemas.sign_in import SignInSchema
from users.schemas.sign_up import SignUpSchema
from users.services.sign_in import login_user
from users.services.sign_up import create_user

router = APIRouter(tags=['auth'])


@router.post("/sign-up")
async def sign_up(
    credentials: Annotated[SignUpSchema, Depends(SchemaDep(SignUpSchema))],
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
    response.delete_cookie(key=settings.app.cookie_key_card)
    return response


@router.post("/sign-in")
async def sign_in(
    credentials: Annotated[SignInSchema, Depends(SchemaDep(SignInSchema))],
    session: SessionDep,
):
    response = Response()
    await login_user(
        session=session, credentials=credentials, response=response
    )
    return response
