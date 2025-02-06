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
    async def get_user_orders(cls, session: AsyncSession, user_id: int):
        # query = select(cls.model).options(
        #     defer(cls.model.full_description),
        #     selectinload(cls.model.reviews).load_only(
        #         ReviewModel.product_id, ReviewModel.rate
        #     ),
        #     joinedload(cls.model.sale).load_only(SaleModel.sale_price),
        #     joinedload(cls.model.category)
        #     .load_only(CategoryModel.id)
        #     .selectinload(CategoryModel.tags),
        #     selectinload(cls.model.images),
        # ) ImageModel

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
        result = await session.execute(query)
        return result.scalars().all()


class OrderProductRepository(ManagerRepository):
    model = OrderProductModel
