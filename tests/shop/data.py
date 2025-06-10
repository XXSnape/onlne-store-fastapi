from pathlib import Path
from json import load


def upload_data(filename: str) -> dict | list:
    path = Path(__file__).resolve().parent / "data" / filename
    with path.open() as file:
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
