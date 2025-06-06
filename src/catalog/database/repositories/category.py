from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from catalog.database import CategoryModel
from core import ManagerRepository


class CategoryRepository(ManagerRepository):
    model = CategoryModel

    @classmethod
    async def get_categories(cls, session: AsyncSession):
        query = (
            select(cls.model)
            .options(
                joinedload(cls.model.image),
                selectinload(cls.model.children, recursion_depth=5).joinedload(
                    cls.model.image
                ),
            )
            .where(cls.model.parent_id.is_(None))
            .order_by(cls.model.id)
        )
        result = await session.execute(query)
        return result.scalars().all()
