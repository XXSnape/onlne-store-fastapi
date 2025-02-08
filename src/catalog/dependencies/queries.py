from decimal import Decimal
from typing import Annotated

from fastapi import Query

from catalog.schemas.catalog import FilterQuerySchema
from catalog.utils.constants import SortingEnum, SortingTypeEnum
from core import settings


def get_filtering_options(
    name: Annotated[
        str | None,
        Query(
            alias="filter[name]",
        ),
    ] = None,
    min_price: Annotated[
        Decimal,
        Query(
            alias="filter[minPrice]",
        ),
    ] = 1,
    max_price: Annotated[
        Decimal | None,
        Query(
            alias="filter[maxPrice]",
            ge=1,
        ),
    ] = None,
    free_delivery: Annotated[
        bool, Query(alias="filter[freeDelivery]")
    ] = False,
    is_available: Annotated[
        bool,
        Query(
            alias="filter[available]",
        ),
    ] = True,
    category_id: Annotated[
        int | None,
        Query(
            alias="category",
        ),
    ] = None,
    sort: Annotated[SortingEnum, Query()] = SortingEnum.date,
    sort_type: Annotated[
        SortingTypeEnum,
        Query(
            alias="sortType",
        ),
    ] = SortingTypeEnum.dec,
    tags: Annotated[
        list[int] | None,
        Query(
            alias="tags[]",
        ),
    ] = None,
    current_page: Annotated[
        int,
        Query(alias="currentPage"),
    ] = 1,
    limit: int = settings.app.limit,
):
    return FilterQuerySchema(
        name=name,
        min_price=min_price,
        max_price=max_price,
        free_delivery=free_delivery,
        is_available=is_available,
        category_id=category_id,
        sort=sort,
        sort_type=sort_type,
        tags=tags,
        current_page=current_page,
        limit=limit,
    )
