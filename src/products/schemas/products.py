from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field
from datetime import datetime

from core import ImageSchema
from .reviews import ReviewSchema
from .tags import TagSchema


class ProductGeneralSchema(BaseModel):
    id: int
    category: Annotated[int, Field(validation_alias="category_id")]
    price: Decimal
    count: int
    date: datetime
    title: str
    description: str
    free_delivery: Annotated[
        bool,
        Field(
            validation_alias="free_delivery",
            serialization_alias="freeDelivery",
        ),
    ]
    images: list[ImageSchema]
    tags: list[TagSchema]
    reviews: Annotated[int, Field(validation_alias="reviews_count")]
    rating: int


class ProductDetailsSchema(ProductGeneralSchema):
    full_description: Annotated[
        str,
        Field(
            validation_alias="full_description",
            serialization_alias="fullDescription",
        ),
    ]
    reviews: list[ReviewSchema]
