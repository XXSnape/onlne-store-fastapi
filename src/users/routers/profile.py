from fastapi import APIRouter, UploadFile
from starlette.responses import Response

from core import UserIdDep, SessionDep
from users.services.avatar import save_avatar
from users.services.profile import get_user_profile

router = APIRouter()


@router.get("/profile")
async def get_profile(user_id: UserIdDep, session: SessionDep):
    return await get_user_profile(session=session, user_id=user_id)
    # return {
    #     "fullName": "Annoying Orange",
    #     "email": "no-reply@mail.ru",
    #     "phone": "88002000600",
    #     "avatar": None,
    # }


@router.post("/profile/avatar")
async def save_user_avatar(
    user_id: UserIdDep, session: SessionDep, avatar: UploadFile
):
    await save_avatar(session=session, user_id=user_id, avatar=avatar)
    return Response()
