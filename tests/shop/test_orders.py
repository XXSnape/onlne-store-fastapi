import datetime

import pytest
from httpx import AsyncClient

from orders.utils.constants import (
    DeliveryTypeEnum,
    PaymentTypeEnum,
    OrderStatusEnum,
)
from .clear_data import clean_orders_from_dates, clean_dates


@pytest.mark.orders
async def test_order_creation_cycle(ac: AsyncClient):
    d = datetime.datetime.now().isoformat()
    orders = await ac.get("api/orders")
    initial_orders_data = orders.json()
    clean_orders_from_dates(initial_orders_data)

    assert initial_orders_data == [
        {
            "id": 1,
            "fullName": "Name Surname",
            "email": "Не указано",
            "phone": "Не указано",
            "deliveryType": "ordinary",
            "paymentType": "online",
            "totalCost": "800.0000",
            "status": "paid",
            "city": "city 1",
            "address": "address 1",
            "products": [
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
                },
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
                },
            ],
        },
        {
            "id": 3,
            "fullName": "Name Surname",
            "email": "Не указано",
            "phone": "Не указано",
            "deliveryType": "ordinary",
            "paymentType": "online",
            "totalCost": "200.0000",
            "status": "unpaid",
            "city": "city 1",
            "address": "address 1",
            "products": [
                {
                    "id": 1,
                    "price": "100.0000",
                    "title": "Product1",
                    "images": [],
                    "category": 1,
                    "count": 2,
                    "description": "Нет описания",
                    "freeDelivery": False,
                    "tags": [
                        {"id": 1, "name": "Tag1"},
                        {"id": 2, "name": "Tag2"},
                    ],
                    "reviews": 0,
                    "rating": 0,
                }
            ],
        },
    ]

    products = [
        {
            "id": 5,
            "price": "500.0000",
            "title": "Product5",
            "date": d,
            "images": [],
            "category": 2,
            "count": 2,
            "description": "Нет описания",
            "freeDelivery": False,
            "tags": [{"id": 1, "name": "Tag1"}],
            "reviews": 1,
            "rating": 2,
        },
        {
            "id": 7,
            "price": "50.0000",
            "title": "Product7",
            "date": d,
            "images": [],
            "category": 1,
            "count": 3,
            "description": "Нет описания",
            "freeDelivery": True,
            "tags": [
                {"id": 1, "name": "Tag1"},
                {"id": 2, "name": "Tag2"},
            ],
            "reviews": 1,
            "rating": 4,
        },
    ]
    response = await ac.post(
        "api/orders",
        json=products,
    )
    data = response.json()
    orders_without_confirmation = await ac.get("api/orders")
    orders_without_confirmation_data = clean_orders_from_dates(
        orders_without_confirmation.json()
    )
    assert orders_without_confirmation_data == initial_orders_data + [
        {
            "id": 4,
            "fullName": "Name Surname",
            "email": "Не указано",
            "phone": "Не указано",
            "deliveryType": None,
            "paymentType": None,
            "totalCost": None,
            "status": "unpaid",
            "city": None,
            "address": None,
            "products": [
                {
                    "id": 5,
                    "price": "500.0000",
                    "title": "Product5",
                    "images": [],
                    "category": 2,
                    "count": 2,
                    "description": "Нет описания",
                    "freeDelivery": False,
                    "tags": [{"id": 1, "name": "Tag1"}],
                    "reviews": 1,
                    "rating": 2,
                },
                {
                    "id": 7,
                    "price": "50.0000",
                    "title": "Product7",
                    "images": [],
                    "category": 1,
                    "count": 3,
                    "description": "Нет описания",
                    "freeDelivery": True,
                    "tags": [
                        {"id": 1, "name": "Tag1"},
                        {"id": 2, "name": "Tag2"},
                    ],
                    "reviews": 1,
                    "rating": 4,
                },
            ],
        }
    ]

    new_order_data = {
        "id": data["orderId"],
        "createdAt": d,
        "fullName": "name",
        "email": "example@gmail.com",
        "phone": "78888888888",
        "deliveryType": DeliveryTypeEnum.express.value,
        "paymentType": PaymentTypeEnum.online.value,
        "totalCost": "1150.0000",
        "status": OrderStatusEnum.unpaid.value,
        "city": "city1",
        "address": "address1",
        "products": products,
    }
    r2 = await ac.post(
        f"api/orders/{data['orderId']}",
        json=new_order_data,
    )
    assert r2.status_code == 200
    orders_with_confirmation = await ac.get("api/orders")
    orders_with_confirmation_data = clean_orders_from_dates(
        orders_with_confirmation.json()
    )
    orders_without_confirmation_data[-1].update(
        deliveryType=DeliveryTypeEnum.express.value,
        paymentType=PaymentTypeEnum.online.value,
        totalCost="1150.0000",
        city="city1",
        address="address1",
    )
    assert orders_with_confirmation_data == orders_without_confirmation_data
    pay_for_order = await ac.post(
        f"api/payment/{data['orderId']}",
        json={
            "number": "1234567890123456",
            "name": "name",
            "month": 9,
            "year": 2030,
            "code": 999,
        },
    )
    assert pay_for_order.status_code == 200
    orders_with_payment = await ac.get("api/orders")
    orders_with_confirmation_data[-1]["status"] = OrderStatusEnum.paid.value
    assert (
        clean_orders_from_dates(orders_with_payment.json())
        == orders_with_confirmation_data
    )
    products = [
        (
            5,
            3,
        ),
        (7, 4),
    ]
    for product_id, count in products:
        response = await ac.get(f"api/product/{product_id}")
        assert response.json()["count"] == count
    order_details_response = await ac.get(f"api/orders/{data['orderId']}")
    order_details_data = order_details_response.json()
    order_details_data.pop("createdAt")
    clean_dates(order_details_data["products"])
    assert order_details_data == {
        "id": 4,
        "fullName": "Name Surname",
        "email": "Не указано",
        "phone": "Не указано",
        "deliveryType": "express",
        "paymentType": "online",
        "totalCost": "1150.0000",
        "status": "paid",
        "city": "city1",
        "address": "address1",
        "products": [
            {
                "id": 5,
                "price": "500.0000",
                "title": "Product5",
                "images": [],
                "category": 2,
                "count": 2,
                "description": "Нет описания",
                "freeDelivery": False,
                "tags": [{"id": 1, "name": "Tag1"}],
                "reviews": 1,
                "rating": 2,
            },
            {
                "id": 7,
                "price": "50.0000",
                "title": "Product7",
                "images": [],
                "category": 1,
                "count": 3,
                "description": "Нет описания",
                "freeDelivery": True,
                "tags": [{"id": 1, "name": "Tag1"}, {"id": 2, "name": "Tag2"}],
                "reviews": 1,
                "rating": 4,
            },
        ],
    }
