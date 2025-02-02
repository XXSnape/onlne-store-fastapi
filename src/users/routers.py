from typing import Annotated

from fastapi import APIRouter, Body, Response, status

from core import SessionDep
from .services.sign_up import create_user

router = APIRouter()


@router.post("/sign-up")
async def sign_up(credentials: Annotated[str, Body()], session: SessionDep):
    await create_user(session=session, credentials=credentials)
    return Response(status_code=status.HTTP_200_OK)
