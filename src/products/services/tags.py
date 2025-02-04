from sqlalchemy.ext.asyncio import AsyncSession

from products.database.repositories.tag_category import TagCategoryRepository
from products.schemas.tags import TagSchema


async def get_tags_by_category_id(session: AsyncSession, category_id: int):
    tags = await TagCategoryRepository.get_tags_by_category_id(
        session=session, category_id=category_id
    )
    return [
        TagSchema.model_validate(tag, from_attributes=True) for tag in tags
    ]
