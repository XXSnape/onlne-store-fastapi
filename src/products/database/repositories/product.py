from typing import Any, Sequence

from sqlalchemy import select, func, or_, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    contains_eager,
    joinedload,
    selectinload,
    defer,
    InstrumentedAttribute,
)

from core import ManagerRepository, settings
from products.database import (
    ProductModel,
    ReviewModel,
    CategoryModel,
    SaleModel,
    TagCategoryModel,
    TagModel,
)
from products.schemas.catalog import FilterQuerySchema
from products.utils.constants import SortingEnum, SortingTypeEnum
from users.database import UserModel


class ProductRepository(ManagerRepository):
    model = ProductModel

    @staticmethod
    def get_sorting_attribute(column, sort_type: SortingTypeEnum):
        return getattr(
            column,
            ("desc" if sort_type == SortingTypeEnum.dec else "asc"),
        )()

    @classmethod
    def get_query_with_cte_filtering(
        cls, query, attribute: InstrumentedAttribute[int], function, sort_type
    ):
        sorting_by_reviews_cte = (
            select(cls.model.id, function(attribute).label("sorting"))
            .join(ReviewModel, cls.model.id == ReviewModel.product_id)
            .group_by(cls.model.id)
        ).cte()
        return query.outerjoin(sorting_by_reviews_cte).order_by(
            cls.get_sorting_attribute(
                column=sorting_by_reviews_cte.c.sorting,
                sort_type=sort_type,
            )
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
        if ids:
            query = query.where(cls.model.id.in_(ids))
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
        if filtering_data.tags:
            products_with_tags = (
                select(cls.model.id)
                .distinct()
                .join(CategoryModel)
                .join(TagCategoryModel)
                .join(TagModel)
                .where(TagModel.id.in_(filtering_data.tags))
            )
            query = query.where(cls.model.id.in_(products_with_tags))

        count_query = select(func.count()).select_from(query.subquery())
        count_result = await session.scalar(count_query)

        if filtering_data.sort == SortingEnum.reviews:
            query = cls.get_query_with_cte_filtering(
                query=query,
                attribute=cls.model.id,
                function=func.count,
                sort_type=filtering_data.sort_type,
            )

        if filtering_data.sort == SortingEnum.rating:
            query = cls.get_query_with_cte_filtering(
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
            )
        if filtering_data.sort == SortingEnum.date:
            query = query.order_by(
                cls.get_sorting_attribute(
                    column=cls.model.date,
                    sort_type=filtering_data.sort_type,
                )
            )
        result = await session.execute(query)
        return result.scalars().all(), count_result


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
