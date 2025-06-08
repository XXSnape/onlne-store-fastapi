from copy import deepcopy

from httpx import AsyncClient
import pytest

from core.utils.jwt import get_access_token
from .clear_data import clear_date


@pytest.mark.review
async def test_review(ac: AsyncClient):
    response = await ac.get("api/product/2")
    product_data = response.json()
    product_data.pop("date")
    assert product_data == {
        "id": 2,
        "price": "200.0000",
        "title": "Product2",
        "images": [],
        "category": 2,
        "count": 10,
        "description": "Нет описания",
        "freeDelivery": False,
        "tags": [{"id": 1, "name": "Tag1"}],
        "reviews": [],
        "rating": 0,
        "fullDescription": "Нет полного описания",
    }
    old_cookies = ac.cookies
    ac.cookies = {
        "access-token": get_access_token(
            user_id=2, username="user2", is_admin=False
        )
    }
    response = await ac.post(
        "api/product/2/reviews", json={"text": "Good Product2", "rate": 5}
    )
    reviews_data = response.json()
    reviews_data_copy = deepcopy(reviews_data)
    assert clear_date(
        reviews_data,
    ) == [
        {
            "email": "Не указано",
            "author": "user2",
            "rate": 5,
            "text": "Good Product2",
        }
    ]
    product_data["reviews"] = reviews_data_copy
    product_data["rating"] = 5
    response = await ac.get("api/product/2")
    result_product_data = response.json()
    result_product_data.pop("date")
    assert result_product_data == product_data
    ac.cookies = old_cookies
