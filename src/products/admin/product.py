from sqladmin import ModelView

from core import UUIDFilenameAdminMixin
from products.database import (
    ProductModel,
    ProductImageModel,
    SaleModel,
    SpecificationModel,
    SpecificationProductModel,
)


class ProductAdmin(ModelView, model=ProductModel):
    column_list = [
        ProductModel.id,
        ProductModel.title,
        ProductModel.price_per_unit,
        ProductModel.count,
        ProductModel.category,
    ]


class ProductImageAdmin(
    UUIDFilenameAdminMixin, ModelView, model=ProductImageModel
):
    column_list = [ProductImageModel.id, ProductImageModel.src]


class SaleAdmin(ModelView, model=SaleModel):
    column_list = [
        SaleModel.id,
        SaleModel.sale_price,
        SaleModel.date_from,
        SaleModel.date_to,
        SaleModel.product,
    ]


class SpecificationAdmin(ModelView, model=SpecificationModel):
    column_list = "__all__"


class SpecificationProductAdmin(ModelView, model=SpecificationProductModel):
    column_list = "__all__"
