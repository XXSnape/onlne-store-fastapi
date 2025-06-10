import pytest
from httpx import AsyncClient
from .data import clean_dates, upload_data

type query_params = dict[str, int | bool | str]


@pytest.mark.parametrize(
    "path, filename",
    [
        ("products/limited", "limited_products.json"),
        ("banners", "banners.json"),
        ("products/popular", "popular_products.json"),
    ],
)
async def test_types_of_products(ac: AsyncClient, path: str, filename: str):
    response = await ac.get(f"api/{path}")
    data = response.json()
    clean_dates(data)
    assert data == upload_data(filename)


async def test_sales(ac: AsyncClient):
    response = await ac.get("api/sales")
    data = response.json()
    clean_dates(data["items"], attrs=("dateFrom",))
    assert data == {
        "currentPage": 1,
        "items": [
            {
                "id": 7,
                "price": "700.0000",
                "title": "Product7",
                "images": [],
                "salePrice": "50.0000",
                "dateTo": "06-09",
            },
            {
                "id": 8,
                "price": "800.0000",
                "title": "Product8",
                "images": [],
                "salePrice": "700.0000",
                "dateTo": "07-09",
            },
        ],
        "lastPage": 1,
    }


@pytest.mark.parametrize(
    "params, filename",
    [
        ({"filter[name]": "prod"}, "name_search.json"),
        ({"filter[minPrice]": 40, "filter[maxPrice]": 650}, "by_prices.json"),
        (
            {
                "filter[minPrice]": 40,
                "filter[maxPrice]": 650,
                "filter[available]": False,
            },
            "priced_and_unavailable.json",
        ),
        (
            {
                "filter[minPrice]": 40,
                "filter[maxPrice]": 650,
                "filter[available]": False,
                "currentPage": 2,
            },
            "priced_and_unavailable_2.json",
        ),
        (
            {
                "filter[minPrice]": 40,
                "filter[maxPrice]": 650,
                "category": 1,
            },
            "search_by_category.json",
        ),
        (
            {
                "filter[minPrice]": 40,
                "filter[maxPrice]": 650,
                "tags[]": [1],
            },
            "search_by_tag.json",
        ),
        (
            {
                "filter[minPrice]": 40,
                "filter[maxPrice]": 650,
                "tags[]": [1, 2],
            },
            "search_by_tags.json",
        ),
        (
            {
                "filter[minPrice]": 40,
                "filter[maxPrice]": 650,
                "filter[freeDelivery]": True,
            },
            "free_delivery_products.json",
        ),
        (
            {
                "filter[minPrice]": 40,
                "filter[maxPrice]": 650,
                "sort": "price",
            },
            "sort_by_price.json",
        ),
        (
            {
                "filter[minPrice]": 40,
                "filter[maxPrice]": 650,
                "sort": "rating",
            },
            "sort_by_rating.json",
        ),
        (
            {
                "filter[minPrice]": 40,
                "filter[maxPrice]": 650,
                "sort": "rating",
                "sortType": "inc",
            },
            "sort_by_rating_increment.json",
        ),
        (
            {
                "filter[minPrice]": 40,
                "filter[maxPrice]": 650,
                "sort": "reviews",
                "filter[available]": False,
            },
            "sort_by_reviews_1.json",
        ),
        (
            {
                "filter[minPrice]": 40,
                "filter[maxPrice]": 650,
                "sort": "reviews",
                "filter[available]": False,
                "currentPage": 2,
            },
            "sort_by_reviews_2.json",
        ),
        (
            {
                "filter[minPrice]": 40,
                "filter[maxPrice]": 650,
                "sort": "price",
                "filter[available]": False,
                "currentPage": 1,
                "sortType": "inc",
                "limit": 20,
            },
            "big_limit.json",
        ),
        (
            {
                "filter[minPrice]": 40,
                "filter[maxPrice]": 650,
                "sort": "price",
                "filter[available]": False,
                "currentPage": 2,
                "sortType": "inc",
                "limit": 2,
            },
            "small_limit.json",
        ),
    ],
)
async def test_catalog(ac: AsyncClient, params: query_params, filename: str):

    response = await ac.get(
        "api/catalog",
        params=params,
    )

    data = response.json()
    clean_dates(data["items"])
    assert data == upload_data(filename=filename)


@pytest.mark.parametrize(
    "params",
    [
        {"filter[name]": "thing"},
        {
            "filter[minPrice]": 801,
        },
        {"filter[maxPrice]": 10},
        {"category": 100},
        {"tags[]": [100]},
        {"currentPage": 3},
    ],
)
async def test_empty_catalog(ac: AsyncClient, params: query_params):
    response = await ac.get(
        "api/catalog",
        params=params,
    )
    current_page = params.get("currentPage", 1)
    last_page = params.get("currentPage")
    if last_page is None:
        last_page = 1
    else:
        last_page = 2
    assert response.json() == {
        "currentPage": current_page,
        "items": [],
        "lastPage": last_page,
    }


async def test_product(ac: AsyncClient):
    response = await ac.get("api/product/8")
    data = response.json()
    data.pop("date")
    clean_dates(data["reviews"])
    assert data == {
        "id": 8,
        "price": "700.0000",
        "title": "Product8",
        "images": [],
        "category": 3,
        "count": 8,
        "description": "Нет описания",
        "freeDelivery": False,
        "tags": [],
        "reviews": [
            {
                "text": "Some text",
                "rate": 5,
                "author": "user1",
                "email": "Не указано",
            }
        ],
        "rating": 5,
        "fullDescription": "Нет полного описания",
        "specifications": [
            {"name": "Spec1", "value": "Value1"},
            {"name": "Spec2", "value": "Value2"},
        ],
    }
