from datetime import date
from decimal import Decimal
from typing import Annotated, Self

from pydantic import (
    AliasChoices,
    BaseModel,
    Field,
    PlainSerializer,
    computed_field,
    model_validator,
)
from pydantic_core.core_schema import ValidationInfo

from core import DateSchema, ImageSchema

from .reviews import ReviewSchema
from .specifications import SpecificationSchema
from .tags import TagSchema

short_date_serializer = PlainSerializer(
    lambda d: d.strftime("%d-%m"), return_type=str
)


class ProductBaseSchema(BaseModel):
    id: int
    price: Decimal
    title: str
    images: list[ImageSchema]


class ProductGeneralSchema(ProductBaseSchema, DateSchema):
    category: Annotated[
        int, Field(validation_alias=AliasChoices("category_id", "category"))
    ]
    count: int
    description: str
    free_delivery: Annotated[
        bool,
        Field(
            validation_alias=AliasChoices("free_delivery", "freeDelivery"),
            serialization_alias="freeDelivery",
        ),
    ]
    tags: list[TagSchema]
    reviews: Annotated[
        int, Field(validation_alias=AliasChoices("reviews_count", "reviews"))
    ]
    rating: int

    @model_validator(mode="after")
    def validate_count_by_context(self, info: ValidationInfo) -> Self:
        if info.context:
            self.count = int(info.context[str(self.id)])
        return self


class ProductDetailsSchema(ProductGeneralSchema):
    full_description: Annotated[
        str,
        Field(
            validation_alias="full_description",
            serialization_alias="fullDescription",
        ),
    ]
    reviews: list[ReviewSchema]
    specifications: list[SpecificationSchema]


class SaleProductsSchema(ProductBaseSchema):
    id: Annotated[
        int, Field(validation_alias="product_id", serialization_alias="id")
    ]
    sale_price: Annotated[
        Decimal,
        Field(
            validation_alias="sale_price",
            serialization_alias="salePrice",
        ),
    ]
    date_from: Annotated[
        date,
        Field(
            validation_alias="date_from",
            serialization_alias="dateFrom",
        ),
        short_date_serializer,
    ]
    date_to: Annotated[
        date,
        Field(
            validation_alias="date_to",
            serialization_alias="dateTo",
        ),
        short_date_serializer,
    ]


class ResultSchema(BaseModel):
    current_page: Annotated[
        int,
        Field(
            validation_alias="current_page", serialization_alias="currentPage"
        ),
    ]
    items_count: Annotated[int, Field(exclude=True)]
    limit: Annotated[int, Field(exclude=True)]

    @computed_field(alias="lastPage")
    @property
    def last_page(self) -> int:
        pages = self.items_count // self.limit
        if pages != 0 and self.items_count % self.limit != 0:
            pages += 1
        return pages or 1


class ResultSaleSchema(ResultSchema):
    items: list[SaleProductsSchema]


class ResultCatalogSchema(ResultSchema):
    items: list[ProductGeneralSchema]
