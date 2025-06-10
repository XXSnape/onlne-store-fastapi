import datetime

import httpx
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from orders.database.repositories.order import OrderRepository
from orders.utils.constants import (
    DeliveryTypeEnum,
    PaymentTypeEnum,
    OrderStatusEnum,
)
from tests.utils import clean_orders_from_dates, clean_dates, upload_data

from copy import deepcopy


async def test_order_creation_cycle(ac: AsyncClient):
    initial_orders_response = await ac.get("api/orders")
    initial_orders_data = initial_orders_response.json()
    clean_orders_from_dates(initial_orders_data)
    user1_orders = upload_data("user1_orders.json")

    assert initial_orders_data == user1_orders
    products = upload_data("products_to_order.json")
    products_without_dates = clean_dates(deepcopy(products))
    response = await ac.post(
        "api/orders",
        json=products,
    )
    created_order_data = response.json()
    orders_without_confirmation_response = await ac.get("api/orders")
    orders_without_confirmation_data = clean_orders_from_dates(
        orders_without_confirmation_response.json()
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
            "products": products_without_dates,
        }
    ]

    new_order_data = {
        "id": created_order_data["orderId"],
        "createdAt": "2025-06-10T19:03:11.294955",
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
    confirm_order_response = await ac.post(
        f"api/orders/{created_order_data['orderId']}",
        json=new_order_data,
    )
    assert confirm_order_response.status_code == httpx.codes.OK
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
    pay_for_order_response = await ac.post(
        f"api/payment/{created_order_data['orderId']}",
        json={
            "number": "1234567890123456",
            "name": "name",
            "month": 9,
            "year": 2030,
            "code": 999,
        },
    )
    assert pay_for_order_response.status_code == httpx.codes.OK
    orders_with_payment_response = await ac.get("api/orders")
    orders_with_confirmation_data[-1]["status"] = OrderStatusEnum.paid.value
    assert (
        clean_orders_from_dates(orders_with_payment_response.json())
        == orders_with_confirmation_data
    )
    leftover_products = [
        (5, 3),
        (7, 4),
    ]
    for index, (product_id, count) in enumerate(leftover_products):
        response = await ac.get(f"api/product/{product_id}")
        assert response.json()["count"] == count
        products[index]["count"] = count
    order_details_response = await ac.get(
        f"api/orders/{created_order_data['orderId']}"
    )
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
        "products": products_without_dates,
    }


async def test_incorrect_total_cost(
    ac: AsyncClient, async_session: AsyncSession
):
    count_before_creation = (
        await OrderRepository.count_number_objects_by_params(
            session=async_session, data={"user_id": 1}
        )
    )
    products = upload_data("products_to_order.json")
    response = await ac.post(
        "api/orders",
        json=products,
    )
    assert response.status_code == httpx.codes.OK
    data = response.json()
    assert (
        await OrderRepository.count_number_objects_by_params(
            session=async_session, data={"user_id": 1}
        )
        == count_before_creation + 1
    )
    new_order_data = {
        "id": data["orderId"],
        "createdAt": datetime.datetime.now().isoformat(),
        "fullName": "name",
        "email": "example@gmail.com",
        "phone": "78888888888",
        "deliveryType": DeliveryTypeEnum.express.value,
        "paymentType": PaymentTypeEnum.online.value,
        "totalCost": "100.0000",
        "status": OrderStatusEnum.unpaid.value,
        "city": "city1",
        "address": "address1",
        "products": products,
    }
    confirm_order_response = await ac.post(
        f"api/orders/{data['orderId']}",
        json=new_order_data,
    )
    assert (
        confirm_order_response.status_code == httpx.codes.UNPROCESSABLE_ENTITY
    )
    assert (
        await OrderRepository.count_number_objects_by_params(
            session=async_session, data={"user_id": 1}
        )
        == count_before_creation
    )


async def test_confirm_paid_order(ac: AsyncClient):
    d = datetime.datetime.now().isoformat()
    products = upload_data("products_to_order.json")
    order_data = {
        "id": 1,
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
    response = await ac.post(
        f"api/orders/1",
        json=order_data,
    )
    assert response.status_code == httpx.codes.NOT_FOUND
