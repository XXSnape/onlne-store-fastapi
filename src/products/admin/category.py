from sqladmin import ModelView

from core import UUIDFilenameAdminMixin
from products.database import (
    CategoryModel,
    CategoryImageModel,
    TagModel,
    TagCategoryModel,
)


class CategoryAdmin(ModelView, model=CategoryModel):
    column_list = [CategoryModel.id, CategoryModel.title]


class CategoryImageAdmin(
    UUIDFilenameAdminMixin, ModelView, model=CategoryImageModel
):
    column_list = [CategoryImageModel.id, CategoryImageModel.src]


class TagAdmin(ModelView, model=TagModel):
    column_list = "__all__"


class TagCategoryAdmin(ModelView, model=TagCategoryModel):
    column_list = "__all__"
