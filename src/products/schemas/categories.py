from pydantic import BaseModel

from core import ImageSchema


class CategorySchema(BaseModel):
    id: int
    title: str
    image: ImageSchema | None


class ParentCategorySchema(CategorySchema):
    subcategories: list[CategorySchema]
