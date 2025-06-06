from httpx import AsyncClient


async def test_limited_products(ac: AsyncClient):
    response = await ac.get("api/products/limited")
    data = response.json()
    for product in data:
        product.pop("date")
    assert data == [
        {
            "id": 1,
            "price": "100.0000",
            "title": "Product1",
            "images": [],
            "category": 1,
            "count": 0,
            "description": "Нет описания",
            "freeDelivery": False,
            "tags": [{"id": 1, "name": "Tag1"}, {"id": 2, "name": "Tag2"}],
            "reviews": 0,
            "rating": 0,
        },
        {
            "id": 3,
            "price": "100.0000",
            "title": "Product3",
            "images": [],
            "category": 3,
            "count": 0,
            "description": "Нет описания",
            "freeDelivery": False,
            "tags": [{"id": 1, "name": "Tag1"}],
            "reviews": 0,
            "rating": 0,
        },
    ]
