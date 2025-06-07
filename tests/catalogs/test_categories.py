from httpx import AsyncClient


async def test_get_categories(ac: AsyncClient):
    response = await ac.get("api/categories")
    assert response.json() == [
        {
            "id": 1,
            "title": "Category1",
            "image": None,
            "subcategories": [
                {"id": 2, "title": "Category2", "image": None},
                {"id": 5, "title": "Category5", "image": None},
                {"id": 4, "title": "Category4", "image": None},
                {"id": 3, "title": "Category3", "image": None},
            ],
        },
        {"id": 6, "title": "Category6", "image": None, "subcategories": []},
    ]
