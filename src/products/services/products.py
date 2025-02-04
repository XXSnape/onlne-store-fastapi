from sqlalchemy.ext.asyncio import AsyncSession

from products.database.repositories.product import (
    ProductRepository,
    SaleRepository,
)
from products.schemas.products import (
    ProductGeneralSchema,
    ProductDetailsSchema,
    SaleProductsSchema,
    ResultSaleSchema,
)


async def get_products(
    session: AsyncSession,
    is_popular: bool = False,
    is_limited: bool = False,
    is_banner: bool = False,
):
    products = await ProductRepository.get_small_info_about_products(
        session=session,
        is_popular=is_popular,
        is_limited=is_limited,
        is_banner=is_banner,
    )
    return [
        ProductGeneralSchema.model_validate(product, from_attributes=True)
        for product in products
    ]


async def get_product_by_id(session: AsyncSession, product_id: int):
    product = await ProductRepository.get_product_by_id(
        session=session, product_id=product_id
    )
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
