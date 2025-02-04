from typing import Annotated

from fastapi import APIRouter, Query

from core import SessionDep, settings
from products.database.repositories.product import ProductRepository
from products.schemas.catalog import FilterQuerySchema
from products.services.products import (
    get_products,
    get_product_by_id,
    get_sales_products,
)

router = APIRouter()


@router.get("/product/{product_id}")
async def get_product(product_id: int, session: SessionDep):
    return await get_product_by_id(session=session, product_id=product_id)


@router.get("/products/popular")
async def popular_product(session: SessionDep):
    return await get_products(session=session, is_popular=True)


@router.get("/products/limited")
async def limited_product(session: SessionDep):
    return await get_products(session=session, is_limited=True)


@router.get("/banners")
async def get_banners(session: SessionDep):
    return await get_products(session=session, is_banner=True)


@router.get("/sales")
async def get_discounted_items(
    session: SessionDep,
    current_page: Annotated[int, Query(alias="currentPage")] = 1,
):
    return await get_sales_products(session=session, current_page=current_page)


@router.get("/catalog")
async def get_catalog(
    session: SessionDep,
    filtering_data: Annotated[FilterQuerySchema, Query()],
):
    return await ProductRepository.get_catalog(
        session=session, filtering_data=filtering_data
    )
    # print("qqq", filtering_data)
    # # return filter.pages.current_page
    # # print(current_page)
    # return await get_products(session=session, is_popular=True)
