from httpx import AsyncClient


def clear_date(products: dict):
    for product in products:
        product.pop("date")


async def test_limited_products(ac: AsyncClient):
    response = await ac.get("api/products/limited")
    data = response.json()
    clear_date(data)
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
            "price": "300.0000",
            "title": "Product3",
            "images": [],
            "category": 3,
            "count": 0,
            "description": "Нет описания",
            "freeDelivery": False,
            "tags": [{"id": 1, "name": "Tag1"}],
            "reviews": 1,
            "rating": 1,
        },
    ]


async def test_banners(ac: AsyncClient):
    response = await ac.get("api/banners")
    data = response.json()
    clear_date(data)
    assert data == [
        {
            "id": 3,
            "price": "300.0000",
            "title": "Product3",
            "images": [],
            "category": 3,
            "count": 0,
            "description": "Нет описания",
            "freeDelivery": False,
            "tags": [{"id": 1, "name": "Tag1"}],
            "reviews": 1,
            "rating": 1,
        },
        {
            "id": 5,
            "price": "500.0000",
            "title": "Product5",
            "images": [],
            "category": 2,
            "count": 5,
            "description": "Нет описания",
            "freeDelivery": False,
            "tags": [],
            "reviews": 1,
            "rating": 2,
        },
        {
            "id": 6,
            "price": "600.0000",
            "title": "Product6",
            "images": [],
            "category": 1,
            "count": 6,
            "description": "Нет описания",
            "freeDelivery": False,
            "tags": [{"id": 1, "name": "Tag1"}, {"id": 2, "name": "Tag2"}],
            "reviews": 1,
            "rating": 5,
        },
        {
            "id": 7,
            "price": "700.0000",
            "title": "Product7",
            "images": [],
            "category": 1,
            "count": 7,
            "description": "Нет описания",
            "freeDelivery": False,
            "tags": [{"id": 1, "name": "Tag1"}, {"id": 2, "name": "Tag2"}],
            "reviews": 1,
            "rating": 4,
        },
        {
            "id": 8,
            "price": "800.0000",
            "title": "Product8",
            "images": [],
            "category": 3,
            "count": 8,
            "description": "Нет описания",
            "freeDelivery": False,
            "tags": [{"id": 1, "name": "Tag1"}],
            "reviews": 1,
            "rating": 5,
        },
    ]


async def test_popular_products(ac: AsyncClient):
    response = await ac.get("api/products/popular")
    data = response.json()
    clear_date(data)
    assert data == [
        {
            "id": 3,
            "price": "300.0000",
            "title": "Product3",
            "images": [],
            "category": 3,
            "count": 0,
            "description": "Нет описания",
            "freeDelivery": False,
            "tags": [{"id": 1, "name": "Tag1"}],
            "reviews": 1,
            "rating": 1,
        },
        {
            "id": 4,
            "price": "400.0000",
            "title": "Product4",
            "images": [],
            "category": 2,
            "count": 4,
            "description": "Нет описания",
            "freeDelivery": False,
            "tags": [],
            "reviews": 2,
            "rating": 1,
        },
        {
            "id": 5,
            "price": "500.0000",
            "title": "Product5",
            "images": [],
            "category": 2,
            "count": 5,
            "description": "Нет описания",
            "freeDelivery": False,
            "tags": [],
            "reviews": 1,
            "rating": 2,
        },
        {
            "id": 6,
            "price": "600.0000",
            "title": "Product6",
            "images": [],
            "category": 1,
            "count": 6,
            "description": "Нет описания",
            "freeDelivery": False,
            "tags": [{"id": 1, "name": "Tag1"}, {"id": 2, "name": "Tag2"}],
            "reviews": 1,
            "rating": 5,
        },
        {
            "id": 7,
            "price": "700.0000",
            "title": "Product7",
            "images": [],
            "category": 1,
            "count": 7,
            "description": "Нет описания",
            "freeDelivery": False,
            "tags": [{"id": 1, "name": "Tag1"}, {"id": 2, "name": "Tag2"}],
            "reviews": 1,
            "rating": 4,
        },
    ]
