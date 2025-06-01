from httpx import AsyncClient


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
    assert profile_response.json() == {
        "fullName": "Name Surname",
        "email": "Не указано",
        "phone": "Не указано",
        "avatar": None,
    }
