import datetime

import pytest
from httpx import AsyncClient
from .clear_data import clear_date


@pytest.mark.orders
async def test_orders(ac: AsyncClient):
    d = datetime.datetime.now().isoformat()

    # orders = await ac.get("api/orders")
    #
    # print("result", orders.json())
    # [
    #     {
    #         "id": 1,
    #         "createdAt": "2025-06-09 19:20:24",
    #         "fullName": "Name Surname",
    #         "email": "Не указано",
    #         "phone": "Не указано",
    #         "deliveryType": "ordinary",
    #         "paymentType": "online",
    #         "totalCost": "400.0000",
    #         "status": "unpaid",
    #         "city": "city 1",
    #         "address": "address 1",
    #         "products": [
    #             {
    #                 "date": "2025-06-09 19:20:24",
    #                 "id": 1,
    #                 "price": "100.0000",
    #                 "title": "Product1",
    #                 "images": [],
    #                 "category": 1,
    #                 "count": 2,
    #                 "description": "Нет описания",
    #                 "freeDelivery": False,
    #                 "tags": [
    #                     {"id": 1, "name": "Tag1"},
    #                     {"id": 2, "name": "Tag2"},
    #                 ],
    #                 "reviews": 0,
    #                 "rating": 0,
    #             }
    #         ],
    #     },
    #     {
    #         "id": 2,
    #         "createdAt": "2025-06-09 19:20:24",
    #         "fullName": "Name Surname",
    #         "email": "Не указано",
    #         "phone": "Не указано",
    #         "deliveryType": "ordinary",
    #         "paymentType": "online",
    #         "totalCost": "1200.0000",
    #         "status": "paid",
    #         "city": "city 1",
    #         "address": "address 1",
    #         "products": [
    #             {
    #                 "date": "2025-06-09 19:20:24",
    #                 "id": 2,
    #                 "price": "200.0000",
    #                 "title": "Product2",
    #                 "images": [],
    #                 "category": 2,
    #                 "count": 2,
    #                 "description": "Нет описания",
    #                 "freeDelivery": False,
    #                 "tags": [{"id": 1, "name": "Tag1"}],
    #                 "reviews": 0,
    #                 "rating": 0,
    #             },
    #             {
    #                 "date": "2025-06-09 19:20:24",
    #                 "id": 3,
    #                 "price": "400.0000",
    #                 "title": "Product4",
    #                 "images": [],
    #                 "category": 2,
    #                 "count": 1,
    #                 "description": "Нет описания",
    #                 "freeDelivery": False,
    #                 "tags": [{"id": 1, "name": "Tag1"}],
    #                 "reviews": 2,
    #                 "rating": 1,
    #             },
    #         ],
    #     },
    # ]
    #
    # products = [
    #     {
    #         "id": 5,
    #         "price": "500.0000",
    #         "title": "Product5",
    #         "date": d,
    #         "images": [],
    #         "category": 2,
    #         "count": 2,
    #         "description": "Нет описания",
    #         "freeDelivery": False,
    #         "tags": [{"id": 1, "name": "Tag1"}],
    #         "reviews": 1,
    #         "rating": 2,
    #     },
    # ]
    # response = await ac.post(
    #     "api/orders",
    #     json=products,
    # )
    # data = response.json()
    # print("resuult", response.status_code, data)
    # # r2 = await ac.post(
    # #     f"api/orders/{data['orderId']}",
    # #     json={
    # #         "id": data["orderId"],
    # #         "createdAt": d,
    # #         "fullName": "name",
    # #         "email": "example@gmail.com",
    # #         "phone": "78888888888",
    # #         "deliveryType": DeliveryTypeEnum.express.value,
    # #         "paymentType": PaymentTypeEnum.online.value,
    # #         "totalCost": "1000.000",
    # #         "status": OrderStatusEnum.unpaid,
    # #         "city": "city1",
    # #         "address": "address1",
    # #         "products": products,
    # #     },
    # # )
    # # assert r2.status_code == 200
