from fastapi import APIRouter

from core import SessionDep
from products.services.products import get_products

router = APIRouter()


@router.get("/product/{product_id}")
async def get_product(product_id: int):
    return {
        "id": 123,
        "category": 55,
        "price": 500.67,
        "count": 12,
        "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
        "title": "video card",
        "description": "description of the product",
        "fullDescription": "full description of the product",
        "freeDelivery": True,
        "images": [{"src": "/3.png", "alt": "Image alt string"}],
        "tags": ["string"],
        "reviews": [
            {
                "author": "Annoying Orange",
                "email": "no-reply@mail.ru",
                "text": "rewrewrwerewrwerwerewrwerwer",
                "rate": 4,
                "date": "2023-05-05 12:12",
            }
        ],
        "specifications": [{"name": "Size", "value": "XL"}],
        "rating": 4.6,
    }


@router.get("/products/popular")
async def popular_product(session: SessionDep):
    return await get_products(session=session, is_popular=True)


@router.get("/products/limited")
async def limited_product(session: SessionDep):
    return await get_products(session=session, is_limited=True)
