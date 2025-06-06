from typing import Sequence

from sqlalchemy import Row, select
from sqlalchemy.ext.asyncio import AsyncSession

from catalog.database import TagCategoryModel, TagModel
from core import ManagerRepository


class TagCategoryRepository(ManagerRepository):
    model = TagCategoryModel

    @classmethod
    async def get_tags_by_category_id(
        cls, session: AsyncSession, category_id: int | None
    ) -> Sequence[Row[tuple[int, str]]]:
        query = (
            select(TagModel.id, TagModel.name)
            .select_from(TagModel)
            .outerjoin(cls.model, cls.model.tag_id == TagModel.id)
            .order_by(TagModel.id)
        ).distinct()
        if category_id:
            query = query.where(cls.model.category_id == category_id)
        result = await session.execute(query)
        return result.all()
