from pathlib import Path
from json import load, dump


def load_data(filename: str, data: dict | list):
    dir = Path(__file__).resolve().parent / "data" / filename
    with dir.open(mode="w") as file:
        return dump(data, file, indent=4, ensure_ascii=False)


def upload_data(filename: str) -> dict:
    dir = Path(__file__).resolve().parent / "data" / filename
    with dir.open() as file:
        return load(file)


def clean_dates(objects: list[dict], attrs=("date",)):
    for obj in objects:
        for attr in attrs:
            obj.pop(attr)
    return objects


def clean_orders_from_dates(orders: list[dict]):
    clean_dates(orders, attrs=("createdAt",))
    for order in orders:
        clean_dates(order["products"])
    return orders


load_data(
    filename="popular_products.json",
    data=[
        {
            "id": 3,
            "price": "300.0000",
            "title": "Product3",
            "images": [],
            "category": 3,
            "count": 0,
            "description": "Нет описания",
            "freeDelivery": False,
            "tags": [],
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
            "tags": [{"id": 1, "name": "Tag1"}],
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
            "tags": [{"id": 1, "name": "Tag1"}],
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
            "price": "50.0000",
            "title": "Product7",
            "images": [],
            "category": 1,
            "count": 7,
            "description": "Нет описания",
            "freeDelivery": True,
            "tags": [{"id": 1, "name": "Tag1"}, {"id": 2, "name": "Tag2"}],
            "reviews": 1,
            "rating": 4,
        },
    ],
)
