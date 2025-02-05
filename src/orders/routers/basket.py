from fastapi import APIRouter
from fastapi import Cookie
from typing import Annotated
from starlette.responses import Response

from core import SessionDep, settings
from orders.dependencies.redis import RedisDep

from orders.schemas.basket import BasketInSchema
from orders.services.product import add_product_to_basket, get_products_in_card

router = APIRouter()


@router.post("/basket")
async def add_product(
    session: SessionDep,
    redis: RedisDep,
    basket_in: BasketInSchema,
    response: Response,
    card_id: Annotated[
        str | None, Cookie(alias=settings.app.cookie_key_card)
    ] = None,
):
    result = await add_product_to_basket(
        session=session,
        redis=redis,
        basket_in=basket_in,
        card_id=card_id,
        response=response,
    )

    return result


@router.get("/basket")
async def get_basket(
    session: SessionDep,
    redis: RedisDep,
    card_id: Annotated[
        str | None, Cookie(alias=settings.app.cookie_key_card)
    ] = None,
):
    if card_id is None:
        return []
    return await get_products_in_card(
        session=session, redis=redis, card_id=card_id
    )
