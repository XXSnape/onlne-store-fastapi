import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "params, result",
    [
        (
            None,
            [
                {"id": 1, "name": "Tag1"},
                {"id": 2, "name": "Tag2"},
                {"id": 3, "name": "Tag3"},
            ],
        ),
        (
            {"category": 1},
            [
                {"id": 1, "name": "Tag1"},
                {"id": 2, "name": "Tag2"},
            ],
        ),
        (
            {"category": 100},
            [],
        ),
    ],
)
async def test_get_tags(
    ac: AsyncClient,
    params: dict[str, str] | None,
    result: list[dict[str, str | int]],
):
    response = await ac.get("api/tags", params=params)
    assert response.json() == result


