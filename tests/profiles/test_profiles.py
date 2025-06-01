import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils.jwt import get_access_token
from users.database.repositories.user import UserRepository
from users.utils.auth import validate_password


async def test_get_profile_without_correct_cookies(ac: AsyncClient):
    resp1 = await ac.post("api/profile")
    assert resp1.status_code == 422
    resp2 = await ac.post(
        "api/profile", cookies={"access-token": "incorrect.token"}
    )
    assert resp2.status_code == 401


async def test_get_profile_with_correct_cookies(ac: AsyncClient):
    response = await ac.post(
        "api/sign-in", json={"username": "user1", "password": "qwerty"}
    )
    access_token = response.cookies["access-token"]
    profile_response = await ac.get(
        "api/profile",
        cookies={"access-token": access_token},
    )
    assert profile_response.status_code == 200
    assert profile_response.json() == {
        "fullName": "Name Surname",
        "email": "Не указано",
        "phone": "Не указано",
        "avatar": None,
    }


async def test_update_profile(ac: AsyncClient, async_session: AsyncSession):
    token = get_access_token(user_id=1, username="user1", is_admin=False)
    data = {
        "fullName": "new",
        "email": "new@mail.com",
        "phone": "79151234567",
    }
    response1 = await ac.post(
        "api/profile",
        json=data,
        cookies={"access-token": token},
    )
    assert response1.status_code == 422
    user = await UserRepository.get_user_profile(
        session=async_session, user_id=1
    )
    assert user.fullname == "Name Surname"
    data.update(fullName="NewName NewSurname")
    response2 = await ac.post(
        "api/profile",
        json=data,
        cookies={"access-token": token},
    )
    assert response2.status_code == 200
    assert response2.json() == data | {"avatar": None}
    await async_session.refresh(user)
    assert (user.fullname, user.email, user.phone) == tuple(data.values())


@pytest.mark.parametrize(
    "data",
    [
        {
            "currentPassword": "incorrect",
            "newPassword": "NewPassword",
        },
        {
            "currentPassword": "qwerty",
            "newPassword": "weak",
        },
    ],
)
async def test_change_password_failed(
    ac: AsyncClient, data: dict[str, str], async_session: AsyncSession
):
    token = get_access_token(user_id=1, username="user1", is_admin=False)
    response = await ac.post(
        "api/profile/password", json=data, cookies={"access-token": token}
    )
    assert response.status_code in (401, 422)
    user = await UserRepository.get_object_by_params(
        session=async_session, data={"id": 1}
    )
    assert (
        validate_password(password="qwerty", hashed_password=user.password)
        is True
    )


async def test_change_password_passed(
    ac: AsyncClient, async_session: AsyncSession
):
    response = await ac.post(
        "api/sign-in", json={"username": "user1", "password": "qwerty"}
    )
    cookies = {"access-token": response.cookies["access-token"]}
    assert response.status_code == 200
    response = await ac.post(
        "api/profile/password",
        json={
            "currentPassword": "qwerty",
            "newPassword": "new-password",
        },
        cookies=cookies,
    )
    assert response.status_code == 200
    response = await ac.post(
        "api/sign-in", json={"username": "user1", "password": "qwerty"}
    )
    assert response.status_code == 401
    response = await ac.post(
        "api/sign-in", json={"username": "user1", "password": "new-password"}
    )
    assert response.status_code == 200
    user = await UserRepository.get_object_by_params(
        session=async_session, data={"id": 1}
    )
    assert (
        validate_password(password="qwerty", hashed_password=user.password)
        is False
    )
    assert (
        validate_password(
            password="new-password", hashed_password=user.password
        )
        is True
    )
