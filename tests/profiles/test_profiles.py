import httpx
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

import re

from core.utils.jwt import get_access_token
from .utils import make_request_to_save_avatar
from users.database.repositories.user import UserRepository
from users.utils.auth import validate_password


async def test_get_profile_without_correct_cookies(ac: AsyncClient):
    request = httpx.Request(
        "GET",
        "http://test/api/profile",
        cookies={
            "access-token": get_access_token(
                user_id=1, username="user1", is_admin=False
            )
            + "abc"
        },
    )
    response = await ac.send(request)
    assert response.status_code == httpx.codes.UNAUTHORIZED


async def test_get_profile_with_correct_cookies(ac: AsyncClient):
    profile_response = await ac.get(
        "api/profile",
    )
    assert profile_response.status_code == httpx.codes.OK
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
    cookies = {
        "access-token": get_access_token(
            user_id=3, username="user3", is_admin=False
        )
    }
    request1 = httpx.Request(
        "POST",
        "http://test/api/profile",
        json=data,
        cookies=cookies,
    )
    response1 = await ac.send(request1)
    assert response1.status_code == httpx.codes.UNPROCESSABLE_ENTITY
    user = await UserRepository.get_user_profile(
        session=async_session, user_id=3
    )
    assert user.fullname == "Name3 Surname3"
    data.update(fullName="NewName NewSurname")
    request2 = httpx.Request(
        "POST",
        "http://test/api/profile",
        json=data,
        cookies=cookies,
    )
    response2 = await ac.send(request2)
    assert response2.status_code == httpx.codes.OK
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
    assert response.status_code in (
        httpx.codes.UNAUTHORIZED,
        httpx.codes.UNPROCESSABLE_ENTITY,
    )
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
    assert response.status_code == httpx.codes.OK
    response = await ac.post(
        "api/profile/password",
        json={
            "currentPassword": "qwerty",
            "newPassword": "new-password",
        },
    )
    assert response.status_code == httpx.codes.OK
    response = await ac.post(
        "api/sign-in", json={"username": "user1", "password": "qwerty"}
    )
    assert response.status_code == httpx.codes.UNAUTHORIZED
    response = await ac.post(
        "api/sign-in", json={"username": "user1", "password": "new-password"}
    )
    assert response.status_code == httpx.codes.OK
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
    assert avatar_response.status_code == httpx.codes.OK
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
    assert avatar_response.status_code == httpx.codes.UNPROCESSABLE_ENTITY
    response = await ac.get("api/profile")
    assert response.json() == json_response1
