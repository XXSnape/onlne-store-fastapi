from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field

from core import settings
from products.utils.constants import SortingEnum, SortingTypeEnum


class FilterQuerySchema(BaseModel):
    name: Annotated[str, Field(validation_alias="filter[name]", default="")]
    min_price: Annotated[
        Decimal,
        Field(validation_alias="filter[minPrice]", ge=0),
    ]
    max_price: Annotated[
        Decimal, Field(validation_alias="filter[maxPrice]", ge=1)
    ]
    free_delivery: Annotated[
        bool, Field(validation_alias="filter[freeDelivery]", default=False)
    ]
    is_available: Annotated[
        bool, Field(validation_alias="available", default=True)
    ]
    category_id: Annotated[
        int | None, Field(validation_alias="category", default=None)
    ]
    sort: SortingEnum = SortingEnum.date
    sort_type: Annotated[
        SortingTypeEnum,
        Field(validation_alias="sortType", default=SortingTypeEnum.dec),
    ]
    tags: Annotated[list[str], Field(default_factory=list)]
    current_page: Annotated[int, Field(validation_alias="currentPage")]
    limit: int = settings.app.limit


class Pages(BaseModel):
    current_page: Annotated[int, Field(validation_alias="currentPage")]
