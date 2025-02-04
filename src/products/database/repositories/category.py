from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core import ManagerRepository
from products.database import CategoryModel, TagModel


class CategoryRepository(ManagerRepository):
    model = CategoryModel

    async def get_tags_by_category_id(
        self, session: AsyncSession, category_id: int | None
    ):
        query = select(TagModel)
