import httpx
from httpx import AsyncClient

from tests.utils import clean_dates


async def test_filling_and_removing_basket(ac: AsyncClient):
    initial_basket = await ac.get("api/basket")
    assert initial_basket.json() == []
    add_product = await ac.post("api/basket", json={"id": 2, "count": 2})
    assert add_product.cookies.get("card-id") is not None
    add_product_data = add_product.json()
    assert clean_dates(add_product_data) == [
        {
            "id": 2,
            "price": "200.0000",
            "title": "Product2",
            "images": [],
            "category": 2,
            "count": 2,
            "description": "Нет описания",
            "freeDelivery": False,
            "tags": [{"id": 1, "name": "Tag1"}],
            "reviews": 0,
            "rating": 0,
        }
    ]

    result_after_1_product = await ac.get("api/basket")
    assert add_product_data == clean_dates(result_after_1_product.json())

    add_product2 = await ac.post("api/basket", json={"id": 4, "count": 1})
    add_product2_data = add_product2.json()
    assert clean_dates(add_product2_data) == add_product_data + [
        {
            "id": 4,
            "price": "400.0000",
            "title": "Product4",
            "images": [],
            "category": 2,
            "count": 1,
            "description": "Нет описания",
            "freeDelivery": False,
            "tags": [{"id": 1, "name": "Tag1"}],
            "reviews": 2,
            "rating": 1,
        }
    ]
    repeated_addition = await ac.post("api/basket", json={"id": 4, "count": 3})
    add_product2_data[-1]["count"] = 3
    repeated_addition_data = repeated_addition.json()
    assert clean_dates(repeated_addition_data) == add_product2_data
    delete_product = await ac.request(
        method="delete", url="api/basket", json={"id": 2, "count": 2}
    )
    delete_product_data = delete_product.json()
    assert clean_dates(delete_product_data) == [repeated_addition_data[-1]]
    result = await ac.get("api/basket")
    assert clean_dates(result.json()) == delete_product_data
    await ac.request(
        method="delete", url="api/basket", json={"id": 4, "count": 3}
    )


async def test_incorrect_data(ac: AsyncClient):
    await ac.post("api/basket", json={"id": 2, "count": 2})
    response = await ac.request(
        method="delete", url="api/basket", json={"id": 1, "count": 2}
    )
    assert response.status_code == httpx.codes.UNPROCESSABLE_ENTITY
    basket = await ac.get("api/basket")
    data = basket.json()
    assert clean_dates(data) == [
        {
            "id": 2,
            "price": "200.0000",
            "title": "Product2",
            "images": [],
            "category": 2,
            "count": 2,
            "description": "Нет описания",
            "freeDelivery": False,
            "tags": [{"id": 1, "name": "Tag1"}],
            "reviews": 0,
            "rating": 0,
        }
    ]
    add_product = await ac.post("api/basket", json={"id": 4, "count": 100})
    assert add_product.status_code == httpx.codes.UNPROCESSABLE_ENTITY
    add_product = await ac.post("api/basket", json={"id": 100, "count": 1})
    assert add_product.status_code == httpx.codes.NOT_FOUND
    basket = await ac.get("api/basket")
    assert clean_dates(basket.json()) == data
