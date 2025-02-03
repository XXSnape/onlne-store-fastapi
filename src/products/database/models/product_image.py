from sqlalchemy.orm import Mapped

from core import BaseModel
from products.database.models.mixins.product import ProductRelationshipMixin


class ProductImageModel(ProductRelationshipMixin, BaseModel):
    __tablename__ = "product_images"
    _back_populates = "images"
    src: Mapped[str]
