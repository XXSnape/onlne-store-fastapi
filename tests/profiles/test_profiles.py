import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

import re

from .utils import make_request_to_save_avatar
from users.database.repositories.user import UserRepository
from users.utils.auth import validate_password


async def test_get_profile_without_correct_cookies(ac: AsyncClient):
    old_cookies = ac.cookies
    ac.cookies = {"access-token": "incorrect.token"}
    resp1 = await ac.get("api/profile")
    assert resp1.status_code == 401
    ac.cookies = old_cookies


async def test_get_profile_with_correct_cookies(ac: AsyncClient):
    profile_response = await ac.get(
        "api/profile",
    )
    assert profile_response.status_code == 200
    assert profile_response.json() == {
        "fullName": "Name Surname",
        "email": "Не указано",
        "phone": "Не указано",
        "avatar": None,
    }


async def test_update_profile(ac: AsyncClient, async_session: AsyncSession):
    data = {
        "fullName": "new",
        "email": "new@mail.com",
        "phone": "79151234567",
    }
    response1 = await ac.post(
        "api/profile",
        json=data,
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
    response = await ac.post("api/profile/password", json=data)
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
    assert response.status_code == 200
    response = await ac.post(
        "api/profile/password",
        json={
            "currentPassword": "qwerty",
            "newPassword": "new-password",
        },
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


async def test_save_new_avatar(ac: AsyncClient, async_session: AsyncSession):
    filename = "good-avatar.png"
    response = await ac.get("api/profile")
    assert response.json()["avatar"] is None
    avatar_response = await make_request_to_save_avatar(
        ac=ac, filename=filename
    )
    assert avatar_response.status_code == 200
    response = await ac.get("api/profile")
    json = response.json()
    assert json["avatar"]["alt"] == filename
    assert (
        re.fullmatch(
            r"uploads/avatars/1_[\w-]{36}_good-avatar.png",
            json["avatar"]["src"],
        )
        is not None
    )


async def test_fail_save_avatar(ac: AsyncClient):
    response = await ac.get("api/profile")
    json_response1 = response.json()
    avatar_response = await make_request_to_save_avatar(
        ac=ac, filename="bad-avatar.txt"
    )
    assert avatar_response.status_code == 422
    response = await ac.get("api/profile")
    assert response.json() == json_response1
