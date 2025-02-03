from sqlalchemy.orm import Mapped

from core import BaseModel
from products.database.models.mixins.product import ProductRelationshipMixin


class SpecificationModel(ProductRelationshipMixin, BaseModel):
    _back_populates = "specifications"
    name: Mapped[str]
    value: Mapped[str]
