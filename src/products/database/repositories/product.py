from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager

from core import ManagerRepository
from products.database import ProductModel, ReviewModel


class ProductRepository(ManagerRepository):
    model = ProductModel

    @classmethod
    def get_popular_products(cls, session: AsyncSession):
        query = (
            select(cls.model)
            .outerjoin(ReviewModel, cls.model.id == ReviewModel.product_id)
            .options(
                contains_eager(cls.model.reviews),
            )
        )
