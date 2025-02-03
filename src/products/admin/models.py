from sqladmin import ModelView
from products.database import (
    CategoryModel,
    ProductModel,
    ProductImageModel,
    CategoryImageModel,
    SaleModel,
)


class CategoryAdmin(ModelView, model=CategoryModel):
    column_list = [CategoryModel.id, CategoryModel.title]


class ProductAdmin(ModelView, model=ProductModel):
    column_list = [
        ProductModel.id,
        ProductModel.title,
        ProductModel.price_per_unit,
        ProductModel.count,
        ProductModel.category,
    ]


class ProductImageAdmin(ModelView, model=ProductImageModel):
    column_list = [ProductImageModel.id, ProductImageModel.src]


class CategoryImageAdmin(ModelView, model=CategoryImageModel):
    column_list = [CategoryImageModel.id, CategoryImageModel.src]


class SaleAdmin(ModelView, model=SaleModel):
    column_list = [
        SaleModel.id,
        SaleModel.sale_price,
        SaleModel.date_from,
        SaleModel.date_to,
        SaleModel.product,
    ]
