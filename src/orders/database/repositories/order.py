from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from catalog.database import (
    ReviewModel,
    SaleModel,
    CategoryModel,
    ProductModel,
)
from core import ManagerRepository, ImageModelMixin
from orders.database import OrderModel, OrderProductModel


class OrderRepository(ManagerRepository):
    model = OrderModel

    @classmethod
    async def get_user_orders(
        cls, session: AsyncSession, user_id: int, order_id: int | None = None
    ):
        query = (
            select(cls.model)
            .options(
                joinedload(cls.model.user),
                selectinload(cls.model.products)
                .joinedload(OrderProductModel.product)
                .selectinload(ProductModel.reviews),
                selectinload(cls.model.products)
                .joinedload(OrderProductModel.product)
                .joinedload(ProductModel.sale),
                selectinload(cls.model.products)
                .joinedload(OrderProductModel.product)
                .joinedload(ProductModel.category)
                .selectinload(CategoryModel.tags),
                selectinload(cls.model.products)
                .joinedload(OrderProductModel.product)
                .selectinload(ProductModel.images),
            )
            .where(cls.model.user_id == user_id)
        )
        if order_id:
            query = query.where(cls.model.id == order_id)
            result = await session.execute(query)
            return result.scalars().one_or_none()
        result = await session.execute(query)
        return result.scalars().all()


class OrderProductRepository(ManagerRepository):
    model = OrderProductModel
