from sqlalchemy.ext.asyncio import AsyncSession

from catalog.schemas.products import ProductGeneralSchema
from orders.database import OrderProductModel
from orders.database.repositories.order import (
    OrderRepository,
)


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
