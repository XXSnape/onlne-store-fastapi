from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field

from catalog.utils.constants import SortingEnum, SortingTypeEnum
from core import settings


class FilterQuerySchema(BaseModel):
    name: str | None
    min_price: Decimal
    max_price: Decimal | None
    free_delivery: bool
    is_available: bool
    category_id: int | None
    sort: SortingEnum = SortingEnum.date
    sort_type: SortingTypeEnum
    tags: list[int] | None

    current_page: int
    limit: int = settings.app.limit


class Pages(BaseModel):
    current_page: Annotated[int, Field(validation_alias="currentPage")]
