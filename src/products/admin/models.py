from sqladmin import ModelView
from products.database import CategoryModel, ProductModel


class CategoryAdmin(ModelView, model=CategoryModel):
    column_list = [CategoryModel.id, CategoryModel.title]


class ProductAdmin(ModelView, model=ProductModel):
    column_list = [
        ProductModel.id,
        ProductModel.title,
        ProductModel.price_per_unit,
        ProductModel.count,
        ProductModel.category_id,
    ]
