import aiofiles
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from users.database.repositories.avatar import AvatarRepository
from users.exceptions.files import incorrect_extension
import aiofiles.os


async def save_avatar_to_disk(avatar: UploadFile, user_id: int):
    if not any(
        avatar.filename.endswith(extension)
        for extension in {"png", "jpg", "jpeg", "webp"}
    ):
        raise incorrect_extension
    path_to_avatar = f"upload/avatars/{user_id}"
    await aiofiles.os.makedirs("src/" + path_to_avatar, exist_ok=True)
    async with aiofiles.open(
        f"src/{path_to_avatar}/{avatar.filename}", mode="wb"
    ) as output_file:
        content = await avatar.read()
        await output_file.write(content)
    return path_to_avatar + f"/{avatar.filename}"


async def save_avatar(
    user_id: int,
    session: AsyncSession,
    avatar: UploadFile,
) -> None:
    path_to_avatar = await save_avatar_to_disk(avatar=avatar, user_id=user_id)
    await AvatarRepository.create_object(
        session=session, data={"src": path_to_avatar, "user_id": user_id}
    )
