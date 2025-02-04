from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from users.database.repositories.avatar import AvatarRepository
from users.exceptions.files import incorrect_extension
import uuid


async def save_avatar(
    user_id: int,
    session: AsyncSession,
    avatar: UploadFile,
) -> None:
    if not any(
        avatar.filename.endswith(extension)
        for extension in {"png", "jpg", "jpeg", "webp"}
    ):
        raise incorrect_extension
    avatar.filename = f"{user_id}_{uuid.uuid4()}_{avatar.filename}"
    avatar_object = await AvatarRepository.get_object_by_params(
        session=session, data={"user_id": user_id}
    )
    if avatar_object:
        await AvatarRepository.update_object_by_params(
            session=session,
            filter_data={"user_id": user_id},
            update_data={"src": avatar},
        )
        return
    await AvatarRepository.create_object(
        session=session, data={"src": avatar, "user_id": user_id}
    )
