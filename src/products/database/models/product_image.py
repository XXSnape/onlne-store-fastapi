from sqlalchemy.orm import Mapped

from core import BaseModel
from products.database.models.product_mixin import ProductRelationshipMixin


class ProductImageModel(ProductRelationshipMixin, BaseModel):
    __tablename__ = "product_images"
    _back_populates_value = "images"
    src: Mapped[str]
