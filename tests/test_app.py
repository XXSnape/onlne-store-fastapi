from httpx import AsyncClient


async def test_1(ac: AsyncClient, access_token: str):
    response = await ac.post(
        "api/basket",
        cookies={"access-token": access_token},
        json={"id": 1, "count": 2},
    )
    print(response.status_code, response.json())
    assert 1 == 1
