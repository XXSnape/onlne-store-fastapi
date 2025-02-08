from sqladmin import ModelView

from catalog.database import (
    CategoryImageModel,
    CategoryModel,
    TagCategoryModel,
    TagModel,
)
from core import UUIDFilenameAdminMixin


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
