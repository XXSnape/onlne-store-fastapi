from pathlib import Path

from httpx import AsyncClient


async def make_request_to_save_avatar(ac: AsyncClient, filename: str):
    path_to_avatar = Path(__file__).resolve().parent / "avatars" / filename
    with path_to_avatar.open(mode="rb") as file:
        files = {"avatar": (filename, file)}
        response = await ac.post("api/profile/avatar", files=files)
    return response
