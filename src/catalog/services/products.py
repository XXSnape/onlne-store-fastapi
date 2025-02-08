from sqlalchemy.ext.asyncio import AsyncSession

from catalog.database.repositories.product import (
    ProductRepository,
    SaleRepository,
)
from catalog.schemas.catalog import FilterQuerySchema
from catalog.schemas.products import (
    ProductDetailsSchema,
    ProductGeneralSchema,
    ResultCatalogSchema,
    ResultSaleSchema,
    SaleProductsSchema,
)
from core.exceptions.not_found import not_found


async def get_products(
    session: AsyncSession,
    is_popular: bool = False,
    is_limited: bool = False,
    is_banner: bool = False,
    ids: list[int] | None = None,
    context: dict | None = None,
):
    products = await ProductRepository.get_small_info_about_products(
        session=session,
        is_popular=is_popular,
        is_limited=is_limited,
        is_banner=is_banner,
        ids=ids,
    )
    return [
        ProductGeneralSchema.model_validate(
            product, from_attributes=True, context=context
        )
        for product in products
    ]


async def get_product_by_id(session: AsyncSession, product_id: int):
    product = await ProductRepository.get_product_by_id(
        session=session, product_id=product_id
    )
    if not product:
        raise not_found
    return ProductDetailsSchema.model_validate(product, from_attributes=True)


async def get_sales_products(session: AsyncSession, current_page: int):
    products, count = await SaleRepository.get_discounted_products(
        session=session, current_page=current_page
    )
    return ResultSaleSchema(
        items=[
            SaleProductsSchema.model_validate(product, from_attributes=True)
            for product in products
        ],
        current_page=current_page,
        items_count=count,
    )


async def get_catalog(
    session: AsyncSession, filtering_data: FilterQuerySchema
):
    products, count = await ProductRepository.get_catalog(
        session=session, filtering_data=filtering_data
    )
    return ResultCatalogSchema(
        items=[
            ProductGeneralSchema.model_validate(product, from_attributes=True)
            for product in products
        ],
        current_page=filtering_data.current_page,
        items_count=count,
    )
