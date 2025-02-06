from sqlalchemy.ext.asyncio import AsyncSession

from catalog.database import CategoryModel
from catalog.database.repositories.category import CategoryRepository
from catalog.schemas.categories import ParentCategorySchema


def get_subcategories(subcategories: list, root: CategoryModel):
    for children in root.children:
        if children.children:
            get_subcategories(subcategories=subcategories, root=children)
        subcategories.append(children)
    return subcategories


async def get_categories_and_subcategories(session: AsyncSession):
    result = await CategoryRepository.get_categories(session)
    categories = []
    for root_category in result:
        children = get_subcategories(subcategories=[], root=root_category)
        root_category.subcategories = children
        categories.append(root_category)
    return [
        ParentCategorySchema.model_validate(category, from_attributes=True)
        for category in categories
    ]
