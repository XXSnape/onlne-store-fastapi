from json import load
from pathlib import Path

from httpx import AsyncClient


def upload_data(filename: str) -> dict | list:
    path = Path(__file__).resolve().parent / "data" / filename
    with path.open() as file:
        return load(file)


def clean_dates(objects: list[dict], attrs=("date",)):
    for obj in objects:
        for attr in attrs:
            obj.pop(attr)
    return objects


def clean_orders_from_dates(orders: list[dict]):
    clean_dates(orders, attrs=("createdAt",))
    for order in orders:
        clean_dates(order["products"])
    return orders


async def make_request_to_save_avatar(ac: AsyncClient, filename: str):
    path_to_avatar = (
        Path(__file__).resolve().parent / "profiles" / "avatars" / filename
    )
    with path_to_avatar.open(mode="rb") as file:
        files = {"avatar": (filename, file)}
        response = await ac.post("api/profile/avatar", files=files)
    return response
