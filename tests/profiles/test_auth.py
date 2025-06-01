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
    assert response.status_code == 422
    assert bool(response.cookies) is False
    count = await UserRepository.count_number_objects_by_params(
        session=async_session, data=None
    )
    assert count == 2


async def test_sign_up_passed(
    ac: AsyncClient,
    async_session: AsyncSession,
):
    response = await ac.post(
        "api/sign-up",
        json={
            "name": "Same Fullname",
            "username": "MyUsername",
            "password": "password",
        },
    )
    assert response.status_code == 200
    assert bool(response.cookies) is True
    count = await UserRepository.count_number_objects_by_params(
        session=async_session, data=None
    )
    assert count == 3
    user = await UserRepository.get_object_by_params(
        session=async_session, data={"username": "MyUsername"}
    )
    assert (
        user.fullname == "Same Fullname"
        and (user.email, user.phone) == ("Не указано",) * 2
        and user.is_admin is False
        and isinstance(user.password, bytes)
    )
    access_token = response.cookies["access-token"]
    profile_response = await ac.get(
        "api/profile",
        cookies={"access-token": access_token},
    )
    assert profile_response.status_code == 200
