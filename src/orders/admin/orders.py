from sqladmin import ModelView
from orders.database import OrderModel, OrderProductModel


class OrderAdmin(ModelView, model=OrderModel):
    column_list = "__all__"


class OrderProductAdmin(ModelView, model=OrderProductModel):
    column_list = "__all__"
