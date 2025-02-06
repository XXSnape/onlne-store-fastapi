from sqlalchemy.ext.asyncio import AsyncSession

from orders.database.repositories.order import OrderRepository


async def add_products_to_new_order(session: AsyncSession, user_id: int):
    order = await OrderRepository.create_object(session=session)
