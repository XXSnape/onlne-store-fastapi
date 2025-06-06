from httpx import AsyncClient


async def test_get_tags(ac: AsyncClient):
    response = await ac.get("api/tags")
    print("DATA", response.json())
    assert response.json() == [
        {"id": 1, "name": "Tag1"},
        {"id": 2, "name": "Tag2"},
        {"id": 3, "name": "Tag3"},
    ]
