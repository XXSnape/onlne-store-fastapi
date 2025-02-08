import asyncio
from typing import Annotated

from fastapi import APIRouter, Query, Depends
from fastapi_cache.decorator import cache

from catalog.schemas.categories import ParentCategorySchema
from catalog.schemas.products import (
    ProductDetailsSchema,
    ProductGeneralSchema,
    ResultCatalogSchema,
)
from core import SessionDep
from catalog.dependencies.queries import get_filtering_options
from catalog.schemas.catalog import FilterQuerySchema
from catalog.services.categories import get_categories_and_subcategories
from catalog.services.products import (
    get_products,
    get_product_by_id,
    get_sales_products,
    get_catalog,
)

router = APIRouter()


@router.get("/product/{product_id}", response_model=ProductDetailsSchema)
async def get_product(product_id: int, session: SessionDep):
    return await get_product_by_id(session=session, product_id=product_id)


@router.get("/products/popular", response_model=list[ProductGeneralSchema])
@cache(expire=60 * 5)
async def popular_product(session: SessionDep):
    return await get_products(session=session, is_popular=True)


@router.get("/products/limited", response_model=list[ProductGeneralSchema])
@cache(expire=60 * 5)
async def limited_product(session: SessionDep):
    await asyncio.sleep(5)
    return await get_products(session=session, is_limited=True)


@router.get("/banners", response_model=list[ProductGeneralSchema])
@cache(expire=60 * 5)
async def get_banners(session: SessionDep):
    return await get_products(session=session, is_banner=True)


@router.get("/sales")
async def get_discounted_items(
    session: SessionDep,
    current_page: Annotated[int, Query(alias="currentPage")] = 1,
):
    return await get_sales_products(session=session, current_page=current_page)


@router.get("/catalog", response_model=ResultCatalogSchema)
@cache(expire=60)
async def get_catalog_of_products(
    session: SessionDep,
    filtering_data: Annotated[
        FilterQuerySchema, Depends(get_filtering_options)
    ],
):
    return await get_catalog(session=session, filtering_data=filtering_data)


@router.get("/categories", response_model=list[ParentCategorySchema])
@cache(expire=60 * 5)
async def get_categories(
    session: SessionDep,
):
    result = await get_categories_and_subcategories(session)
    return result
