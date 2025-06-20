import httpx
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from users.database.repositories.user import UserRepository


@pytest.mark.parametrize(
    "data",
    [
        {
            "name": "Fullname",
            "username": "MyUsername",
            "password": "DifficultPassword",
        },
        {
            "name": "Same Fullname",
            "username": "user1",
            "password": "DifficultPassword",
        },
        {
            "name": "Same Fullname",
            "username": "MyUsername",
            "password": "psw",
        },
        {},
    ],
)
async def test_sign_up_failed(
    ac: AsyncClient, async_session: AsyncSession, data: dict[str, str]
):
    response = await ac.post("api/sign-up", json=data)
    assert response.status_code == httpx.codes.UNPROCESSABLE_ENTITY
    assert bool(response.cookies) is False
    count = await UserRepository.count_number_objects_by_params(
        session=async_session, data=None
    )
    assert count == 3


async def test_sign_up_passed(
    ac: AsyncClient,
    async_session: AsyncSession,
):
    response = await ac.post(
        "api/sign-up",
        json={
            "name": "Same Fullname",
            "username": "user4",
            "password": "password",
        },
    )
    assert response.status_code == httpx.codes.OK
    count = await UserRepository.count_number_objects_by_params(
        session=async_session, data=None
    )
    assert count == 4
    user = await UserRepository.get_object_by_params(
        session=async_session, data={"username": "user4"}
    )
    assert (
        user.fullname == "Same Fullname"
        and (user.email, user.phone) == ("Не указано",) * 2
        and user.is_admin is False
        and isinstance(user.password, bytes)
    )
    profile_response = await ac.get(
        "api/profile",
    )
    assert profile_response.status_code == httpx.codes.OK


async def test_sign_out(ac: AsyncClient):
    response = await ac.post(
        "api/sign-out",
    )
    assert response.status_code == httpx.codes.OK


@pytest.mark.parametrize(
    "data",
    [
        {
            "username": "user100",
            "password": "DifficultPassword",
        },
        {
            "username": "user1",
            "password": "incorrectpsw",
        },
    ],
)
async def test_sign_in_failed(ac: AsyncClient, data: dict[str, str]):
    response = await ac.post("api/sign-in", json=data)
    assert response.status_code == httpx.codes.UNAUTHORIZED
    assert bool(response.cookies) is False


async def test_sign_in_passed(ac: AsyncClient):
    response = await ac.post(
        "api/sign-in", json={"username": "user1", "password": "qwerty"}
    )
    assert response.status_code == httpx.codes.OK
    profile_response = await ac.get(
        "api/profile",
    )
    assert profile_response.status_code == httpx.codes.OK
