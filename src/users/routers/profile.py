from fastapi import APIRouter, UploadFile, Body
from typing import Annotated
from starlette.responses import Response

from core import UserIdDep, SessionDep
from users.schemas.password import ChangePasswordSchema
from users.schemas.profile import ProfileInSchema, ProfileSchema
from users.services.avatar import save_avatar
from users.services.password import change_user_password
from users.services.profile import get_user_profile, update_user_profile

router = APIRouter()


@router.get("/profile", response_model=ProfileSchema)
async def get_profile(user_id: UserIdDep, session: SessionDep):
    return await get_user_profile(session=session, user_id=user_id)


@router.post("/profile/avatar")
async def save_user_avatar(
    user_id: UserIdDep, session: SessionDep, avatar: UploadFile
):
    await save_avatar(session=session, user_id=user_id, avatar=avatar)
    return Response()


@router.post("/profile", response_model=ProfileSchema)
async def update_profile(
    user_id: UserIdDep, session: SessionDep, profile_in: ProfileInSchema
):
    await update_user_profile(
        session=session, user_id=user_id, profile_in=profile_in
    )
    return await get_user_profile(session=session, user_id=user_id)


@router.post("/profile/password")
async def change_password(
    user_id: UserIdDep,
    session: SessionDep,
    new_credentials_in: ChangePasswordSchema,
):
    await change_user_password(
        session=session, user_id=user_id, change_password_in=new_credentials_in
    )
    return Response()
