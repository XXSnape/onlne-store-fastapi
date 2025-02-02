from fastapi import APIRouter, UploadFile

from core import UserIdDep, SessionDep

router = APIRouter()


@router.get("/profile")
async def get_profile(user_id: UserIdDep):
    return {
        "fullName": "Annoying Orange",
        "email": "no-reply@mail.ru",
        "phone": "88002000600",
        "avatar": None,
    }


@router.post("/profile/avatar")
async def save_avatar(
    user_id: UserIdDep, session: SessionDep, avatar: UploadFile
):
    print(avatar.filename)
    return "hello"
