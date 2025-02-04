from typing import Final

from sqlalchemy.orm import Mapped

from core import BaseModel, ImageModelMixin
from products.database.models.mixins.product import ProductRelationshipMixin

DIRECTORY_OF_IMAGES: Final[str] = "products"


class ProductImageModel(ProductRelationshipMixin, ImageModelMixin, BaseModel):
    __tablename__ = "product_images"
    _back_populates = "images"
    _directory = DIRECTORY_OF_IMAGES
