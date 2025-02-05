from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field, AliasChoices

from core import settings
from products.utils.constants import SortingEnum, SortingTypeEnum


class FilterQuerySchema(BaseModel):
    name: Annotated[
        str,
        Field(
            validation_alias=AliasChoices("filter[name]", "name"), default=""
        ),
    ]
    min_price: Annotated[
        Decimal,
        Field(
            validation_alias=AliasChoices("filter[minPrice]", "min_price"),
            default=1,
            ge=0,
        ),
    ]
    max_price: Annotated[
        Decimal | None,
        Field(
            validation_alias=AliasChoices("filter[maxPrice]", "max_price"),
            ge=1,
            default=None,
        ),
    ]
    free_delivery: Annotated[
        bool,
        Field(
            validation_alias=AliasChoices(
                "filter[freeDelivery]", "free_delivery"
            ),
            default=False,
        ),
    ]
    is_available: Annotated[
        bool,
        Field(
            validation_alias=AliasChoices("available", "is_available"),
            default=True,
        ),
    ]
    category_id: Annotated[
        int | None,
        Field(
            validation_alias=AliasChoices("category", "category_id"),
            default=None,
        ),
    ]
    sort: SortingEnum = SortingEnum.date
    sort_type: Annotated[
        SortingTypeEnum,
        Field(
            validation_alias=AliasChoices("sortType", "sort_type"),
            default=SortingTypeEnum.dec,
        ),
    ]
    tags: Annotated[
        list[int],
        Field(
            validation_alias=AliasChoices("tags", "tags[]"),
            # default_factory=list,
        ),
    ]
    current_page: Annotated[
        int,
        Field(validation_alias=AliasChoices("currentPage", "current_page")),
    ]
    limit: int = settings.app.limit


class Pages(BaseModel):
    current_page: Annotated[int, Field(validation_alias="currentPage")]
