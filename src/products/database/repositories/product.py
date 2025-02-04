from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    contains_eager,
    joinedload,
    selectinload,
    load_only,
    defer,
)

from core import ManagerRepository, settings
from products.database import (
    ProductModel,
    ReviewModel,
    CategoryModel,
    SaleModel,
)
from users.database import UserModel


class ProductRepository(ManagerRepository):
    model = ProductModel

    @classmethod
    async def get_small_info_about_products(
        cls,
        session: AsyncSession,
        is_popular: bool = False,
        is_limited: bool = False,
        is_banner: bool = False,
    ):
        subquery = (
            select(cls.model.id)
            .outerjoin(ReviewModel, cls.model.id == ReviewModel.product_id)
            .group_by(cls.model.id)
            .limit(5)
        )
        query = select(cls.model).options(
            defer(cls.model.full_description),
            selectinload(cls.model.reviews).load_only(
                ReviewModel.product_id, ReviewModel.rate
            ),
            joinedload(cls.model.sale).load_only(SaleModel.sale_price),
            joinedload(cls.model.category)
            .load_only(CategoryModel.id)
            .selectinload(CategoryModel.tags),
            selectinload(cls.model.images),
        )

        if is_popular:
            popular_products = subquery.order_by(
                func.count(cls.model.id).desc()
            )
            query = query.where(cls.model.id.in_(popular_products))

        if is_banner:
            banners_products = subquery.order_by(
                func.count(ReviewModel.rate).desc()
            )
            query = query.where(cls.model.id.in_(banners_products))

        if is_limited:
            query = query.where(cls.model.count == 0)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_product_by_id(cls, session: AsyncSession, product_id: int):
        query = (
            select(cls.model)
            .options(
                selectinload(cls.model.reviews)
                .joinedload(ReviewModel.user)
                .load_only(UserModel.username, UserModel.email),
                joinedload(cls.model.sale).load_only(SaleModel.sale_price),
                joinedload(cls.model.category)
                .load_only(CategoryModel.id)
                .selectinload(CategoryModel.tags),
                selectinload(cls.model.images),
                selectinload(cls.model.specifications),
            )
            .where(cls.model.id == product_id)
        )
        result = await session.execute(query)
        return result.scalars().one_or_none()


class SaleRepository(ManagerRepository):
    model = SaleModel

    @classmethod
    async def get_discounted_products(
        cls, session: AsyncSession, current_page: int
    ) -> tuple[list[SaleModel], int]:
        count_query = select(func.count()).select_from(cls.model)
        count_result = await session.scalar(count_query)
        query = (
            select(cls.model)
            .options(
                joinedload(cls.model.product)
                .load_only(
                    ProductModel.id,
                    ProductModel.title,
                    ProductModel.price_per_unit,
                )
                .selectinload(ProductModel.images)
            )
            .offset((current_page - 1) * settings.app.limit)
            .limit(settings.app.limit)
        )
        result = await session.execute(query)
        return result.scalars().all(), count_result
