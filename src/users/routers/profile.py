from fastapi import APIRouter, UploadFile
from starlette.responses import Response

from core import UserIdDep, SessionDep
from users.schemas.profile import ProfileSchema, ProfileInSchema
from users.services.avatar import save_avatar
from users.services.profile import get_user_profile, update_user_profile

router = APIRouter()


@router.get("/profile")
async def get_profile(user_id: UserIdDep, session: SessionDep):
    return await get_user_profile(session=session, user_id=user_id)


@router.post("/profile/avatar")
async def save_user_avatar(
    user_id: UserIdDep, session: SessionDep, avatar: UploadFile
):
    await save_avatar(session=session, user_id=user_id, avatar=avatar)
    return Response()


@router.post("/profile")
async def update_profile(
    user_id: UserIdDep, session: SessionDep, profile_in: ProfileInSchema
):
    print("profile", profile_in)
    await update_user_profile(
        session=session, user_id=user_id, profile_in=profile_in
    )
