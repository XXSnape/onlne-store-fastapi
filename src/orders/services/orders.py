from sqlalchemy.ext.asyncio import AsyncSession

from catalog.database.repositories.product import ProductRepository
from catalog.schemas.products import ProductGeneralSchema
from core.exceptions.not_found import (
    not_found,
    no_product_with_these_parameters_was_found,
)
from orders.database import OrderModel, OrderProductModel
from orders.database.repositories.order import (
    OrderProductRepository,
    OrderRepository,
)
from orders.schemas.orders import OrderInSchema, OrdersSchema
from orders.utils.constants import OrderStatusEnum


async def add_products_to_new_order(
    session: AsyncSession,
    user_id: int,
    products: list[ProductGeneralSchema],
):
    order_id = await OrderRepository.create_object(
        session=session, data={"user_id": user_id}
    )
    session.add_all(
        [
            OrderProductModel(
                product_id=product.id, order_id=order_id, count=product.count
            )
            for product in products
        ]
    )
    await session.commit()
    return order_id


async def add_details_to_order(
    session: AsyncSession,
    order_id: int,
    user_id: int,
    order_details: OrderInSchema,
):
    order: OrderModel = await OrderRepository.get_order_with_products(
        session=session,
        order_id=order_id,
        user_id=user_id,
    )
    summ = sum(
        product_in_details.count * product_in_details.product.price
        for product_in_details in order.products
    )
    if summ != order_details.total_cost:
        await session.delete(order)
        await session.commit()
        raise no_product_with_these_parameters_was_found

    order.delivery_type = order_details.delivery_type
    order.payment_type = order_details.payment_type
    order.total_cost = order_details.total_cost
    order.city = order_details.city
    order.address = order_details.address
    await session.commit()


async def get_user_orders(session: AsyncSession, user_id: int):
    orders = await OrderRepository.get_user_orders(
        session=session, user_id=user_id
    )
    return [
        OrdersSchema.model_validate(order, from_attributes=True)
        for order in orders
    ]


async def get_user_order(session: AsyncSession, user_id: int, order_id: int):
    order = await OrderRepository.get_user_orders(
        session=session,
        user_id=user_id,
        order_id=order_id,
    )
    if order is None:
        raise not_found
    return OrdersSchema.model_validate(order, from_attributes=True)


async def pay_order(session: AsyncSession, user_id: int, order_id: int):
    order: OrderModel = await OrderRepository.get_object_by_params(
        session=session,
        data={
            "id": order_id,
            "user_id": user_id,
            "status": OrderStatusEnum.unpaid,
        },
    )
    if not order:
        raise not_found
    await OrderProductRepository.update_products_quantity(session, order_id)
    order.status = OrderStatusEnum.paid
    await session.commit()
