from core import ManagerRepository
from orders.database import OrderModel, OrderProductModel


class OrderRepository(ManagerRepository):
    model = OrderModel


class OrderProductRepository(ManagerRepository):
    model = OrderProductModel
