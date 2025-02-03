from sqlalchemy.ext.asyncio import AsyncSession

from products.database.repositories.product import ProductRepository
from products.schemas.products import ProductGeneralSchema


async def get_products(
    session: AsyncSession, is_popular: bool = False, is_limited: bool = False
):
    products = await ProductRepository.get_small_info_about_products(
        session=session, is_popular=is_popular, is_limited=is_limited
    )
    return [
        ProductGeneralSchema.model_validate(product, from_attributes=True)
        for product in products
    ]
