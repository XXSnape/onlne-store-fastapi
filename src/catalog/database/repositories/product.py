from decimal import Decimal
from typing import Sequence

from sqlalchemy import Row, asc, desc, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    InstrumentedAttribute,
    contains_eager,
    defer,
    joinedload,
    selectinload,
)
from sqlalchemy.sql.functions import coalesce

from catalog.database import (
    CategoryModel,
    ProductModel,
    ReviewModel,
    SaleModel,
    TagCategoryModel,
)
from catalog.schemas.catalog import FilterQuerySchema
from catalog.utils.constants import SortingEnum, SortingTypeEnum
from core import ManagerRepository, settings
from orders.database import OrderModel, OrderProductModel
from orders.utils.constants import OrderStatusEnum
from users.database import UserModel


class ProductRepository(ManagerRepository):
    model = ProductModel

    @staticmethod
    def get_sorting_attribute(
        column, sort_type: SortingTypeEnum, add_coalesce: bool = False
    ):
        func = desc if sort_type == SortingTypeEnum.dec else asc
        if add_coalesce:
            return func(coalesce(column, 0))
        return func(
            column,
        )

    @classmethod
    def get_query_with_ordering(
        cls, query, attribute: InstrumentedAttribute[int], function, sort_type
    ):
        subq = (
            select(
                function(attribute).label("sorting"),
            )
            .where(ReviewModel.product_id == cls.model.id)
            .group_by(cls.model.id)
        ).scalar_subquery()
        return query.order_by(
            cls.get_sorting_attribute(
                column=subq, sort_type=sort_type, add_coalesce=True
            ),
            cls.model.id,
        )

    @classmethod
    async def get_small_info_about_products(
        cls,
        session: AsyncSession,
        is_popular: bool = False,
        is_limited: bool = False,
        is_banner: bool = False,
        ids: list[int] | None = None,
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
            popular_products = subquery.where(ReviewModel.id != None).order_by(
                func.count(cls.model.id).desc(), cls.model.id
            )
            query = query.where(cls.model.id.in_(popular_products))

        if is_banner:
            banners_products = subquery.order_by(
                coalesce(func.avg(ReviewModel.rate), 0).desc(), cls.model.id
            )
            query = query.where(cls.model.id.in_(banners_products))

        if is_limited:
            query = query.where(cls.model.count == 0)
        if ids:
            query = query.where(cls.model.id.in_(ids))
        query = query.order_by(cls.model.id)
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
    ) -> tuple[Sequence[ProductModel], int]:
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
            query = query.where(cls.model.title.icontains(filtering_data.name))
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
        if filtering_data.tags:
            subq = (
                select(1)
                .select_from(TagCategoryModel)
                .join(CategoryModel)
                .where(
                    CategoryModel.id == cls.model.category_id,
                    TagCategoryModel.tag_id.in_(filtering_data.tags),
                )
                .having(
                    func.count(TagCategoryModel.tag_id.distinct())
                    >= len(filtering_data.tags)
                )
            ).exists()
            query = query.where(subq)

        count_query = select(func.count()).select_from(query.subquery())
        count_result = await session.scalar(count_query)

        if filtering_data.sort == SortingEnum.reviews:
            query = cls.get_query_with_ordering(
                query=query,
                attribute=ReviewModel.id,
                function=func.count,
                sort_type=filtering_data.sort_type,
            )

        if filtering_data.sort == SortingEnum.rating:
            query = cls.get_query_with_ordering(
                query=query,
                attribute=ReviewModel.rate,
                function=func.avg,
                sort_type=filtering_data.sort_type,
            )
        if filtering_data.sort == SortingEnum.price:
            query = query.order_by(
                cls.get_sorting_attribute(
                    column=SaleModel.sale_price,
                    sort_type=filtering_data.sort_type,
                ),
                cls.get_sorting_attribute(
                    column=cls.model.price_per_unit,
                    sort_type=filtering_data.sort_type,
                ),
                cls.model.id,
            )
        if filtering_data.sort == SortingEnum.date:
            query = query.order_by(
                cls.get_sorting_attribute(
                    column=cls.model.date,
                    sort_type=filtering_data.sort_type,
                ),
                cls.model.id,
            )
        query = query.offset(
            (filtering_data.current_page - 1) * filtering_data.limit
        ).limit(filtering_data.limit)
        result = await session.execute(query)
        return result.scalars().all(), count_result

    @classmethod
    async def is_there_purchase(
        cls, session: AsyncSession, product_id: int, user_id: int
    ):
        query = (
            select(func.count())
            .select_from(OrderProductModel)
            .join(OrderModel)
            .where(
                OrderProductModel.product_id == product_id,
                OrderModel.status == OrderStatusEnum.paid,
                OrderModel.user_id == user_id,
            )
        )
        result = await session.scalar(query)
        return result > 0

    @classmethod
    async def get_product_reviews(cls, session: AsyncSession, product_id: int):
        query = (
            select(cls.model)
            .options(
                selectinload(cls.model.reviews).joinedload(ReviewModel.user)
            )
            .where(cls.model.id == product_id)
        )
        result = await session.execute(query)
        return result.scalars().one().reviews

    @classmethod
    async def get_price_of_goods(
        cls, session: AsyncSession, ids: list[int]
    ) -> Sequence[Row[tuple[int, Decimal]]]:
        query = (
            select(cls.model.id, cls.model.price)
            .options(
                joinedload(cls.model.sale).load_only(SaleModel.sale_price)
            )
            .where(cls.model.id.in_(ids))
        )
        result = await session.execute(query)
        return result.all()


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
