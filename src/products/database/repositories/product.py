from sqlalchemy import select, func, or_
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
from products.schemas.catalog import FilterQuerySchema
from products.utils.constants import SortingEnum
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
                func.avg(ReviewModel.rate).desc()
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

    @classmethod
    async def get_catalog(
        cls, session: AsyncSession, filtering_data: FilterQuerySchema
    ):
        query = (
            select(cls.model)
            .outerjoin(SaleModel)
            .options(
                defer(cls.model.full_description),
                selectinload(cls.model.reviews).load_only(
                    ReviewModel.product_id, ReviewModel.rate
                ),
                contains_eager(cls.model.sale),
                joinedload(cls.model.category)
                .load_only(CategoryModel.id)
                .selectinload(CategoryModel.tags),
                selectinload(cls.model.images),
            )
        )
        if filtering_data.name:
            query = query.where(cls.model.title.contains(filtering_data.name))
        if filtering_data.min_price:
            query = query.where(
                cls.model.price_per_unit >= filtering_data.min_price,
            )
        if filtering_data.max_price:
            query = query.where(
                or_(
                    cls.model.price_per_unit <= filtering_data.max_price,
                    SaleModel.sale_price <= filtering_data.max_price,
                )
            )
        if filtering_data.free_delivery:
            query = query.where(cls.model.free_delivery == True)
        if filtering_data.is_available:
            query = query.where(cls.model.count > 0)
        if filtering_data.category_id:
            query = query.where(
                cls.model.category_id == filtering_data.category_id
            )
        if filtering_data.sort == SortingEnum.reviews:
            subquery = (
                select(
                    cls.model.id, func.avg(ReviewModel.rate).label("review")
                )
                .outerjoin(ReviewModel, cls.model.id == ReviewModel.product_id)
                .group_by(cls.model.id)
            ).subquery()
            query = query.join(subquery).order_by(subquery.c.review.desc())

        result = await session.execute(query)
        return []


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
