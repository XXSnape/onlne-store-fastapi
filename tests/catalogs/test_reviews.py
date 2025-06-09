from copy import deepcopy

import httpx
from httpx import AsyncClient
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from catalog.database.repositories.review import ReviewRepository
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
        "specifications": [],
        "rating": 0,
        "fullDescription": "Нет полного описания",
    }
    request = httpx.Request(
        "POST",
        "http://test/api/product/2/reviews",
        json={"text": "Good Product2", "rate": 5},
        cookies={
            "access-token": get_access_token(
                user_id=2, username="user2", is_admin=False
            )
        },
    )
    response = await ac.send(request)
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


@pytest.mark.review
@pytest.mark.parametrize("product_id", (1, 4))
async def test_fail_repeat_review(
    ac: AsyncClient, async_session: AsyncSession, product_id: int
):
    reviews_count_before_request = (
        await ReviewRepository.count_number_objects_by_params(
            session=async_session, data={"product_id": product_id}
        )
    )
    response = await ac.get(f"api/product/{product_id}")
    make_review_response = await ac.post(
        f"api/product/{product_id}/reviews",
        json={"text": "Good Product4", "rate": 5},
    )
    assert make_review_response.status_code == httpx.codes.UNPROCESSABLE_ENTITY
    the_same_response = await ac.get(f"api/product/{product_id}")
    assert response.json() == the_same_response.json()
    assert (
        reviews_count_before_request
        == await ReviewRepository.count_number_objects_by_params(
            session=async_session, data={"product_id": product_id}
        )
    )
