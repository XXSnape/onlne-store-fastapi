from fastapi import APIRouter, Response
from fastapi import Cookie
from typing import Annotated
from starlette.responses import Response, JSONResponse

from core import SessionDep, settings
from orders.dependencies.redis import RedisDep

from orders.schemas.basket import BasketInSchema
from orders.services.product import add_product_to_basket

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
