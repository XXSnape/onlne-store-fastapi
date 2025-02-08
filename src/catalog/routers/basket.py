from fastapi import APIRouter
from fastapi import Cookie
from typing import Annotated
from starlette.responses import Response

from catalog.schemas.products import ProductGeneralSchema
from core import SessionDep, settings
from catalog.dependencies.redis import RedisDep

from catalog.schemas.basket import BasketInSchema
from catalog.services.basket import (
    get_products_in_card,
    delete_product_from_basket,
    add_product_to_basket,
)

router = APIRouter()


@router.post("/basket", response_model=list[ProductGeneralSchema])
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


@router.get("/basket", response_model=list[ProductGeneralSchema])
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


@router.delete("/basket", response_model=list[ProductGeneralSchema])
async def delete_product(
    session: SessionDep,
    redis: RedisDep,
    basket_in: BasketInSchema,
    response: Response,
    card_id: Annotated[
        str | None, Cookie(alias=settings.app.cookie_key_card)
    ] = None,
):
    if card_id is None:
        return []
    return await delete_product_from_basket(
        session=session,
        redis=redis,
        product_id=basket_in.id,
        response=response,
        card_id=card_id,
    )
