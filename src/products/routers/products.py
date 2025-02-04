from fastapi import APIRouter

from core import SessionDep
from products.services.products import get_products

router = APIRouter()


@router.get("/product/{product_id}")
async def get_product(product_id: int):
    return ...


@router.get("/products/popular")
async def popular_product(session: SessionDep):
    return await get_products(session=session, is_popular=True)


@router.get("/products/limited")
async def limited_product(session: SessionDep):
    return await get_products(session=session, is_limited=True)
