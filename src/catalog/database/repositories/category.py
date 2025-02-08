from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from core import ManagerRepository
from catalog.database import CategoryModel


class CategoryRepository(ManagerRepository):
    model = CategoryModel

    @classmethod
    async def get_categories(cls, session: AsyncSession):
        query = (
            select(CategoryModel)
            .options(
                joinedload(CategoryModel.image),
                selectinload(
                    CategoryModel.children, recursion_depth=5
                ).joinedload(CategoryModel.image),
            )
            .where(CategoryModel.parent_id.is_(None))
        )
        result = await session.execute(query)
        return result.scalars().all()
