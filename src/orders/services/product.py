from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Cookie
from sqlalchemy.sql.annotation import Annotated
from starlette.responses import Response

from core import settings
from redis.asyncio import Redis
from orders.exceptions.count import too_many_products
from orders.schemas.basket import BasketInSchema
from secrets import token_urlsafe
from products.database.repositories.product import ProductRepository
from products.services.products import get_products


async def get_products_in_card(
    session: AsyncSession, redis: Redis, card_id: str
):
    card = await redis.hgetall(card_id)
    return await get_products(
        session=session, ids=[int(id) for id in card.keys()]
    )


async def add_product_to_basket(
    session: AsyncSession,
    redis: Redis,
    basket_in: BasketInSchema,
    response: Response,
    card_id: Annotated[
        str | None, Cookie(alias=settings.app.cookie_key_card)
    ] = None,
):
    key_product = f"product_{basket_in.id}"
    product_quantity = await redis.get(key_product)
    if product_quantity is None:
        product_quantity = await get_product_quantity(
            session=session, product_id=basket_in.id
        )
        await redis.set(key_product, product_quantity, ex=40)
    if int(product_quantity) < basket_in.count:
        raise too_many_products
    if card_id is None:
        card_id = token_urlsafe(32)
        await redis.hset(card_id, mapping={str(basket_in.id): basket_in.count})
        response.set_cookie(
            key=settings.app.cookie_key_card, value=card_id, httponly=True
        )
        return await get_products(session=session, ids=[basket_in.id])
    card = await redis.hgetall(card_id)
    card[str(basket_in.id)] = basket_in.count
    await redis.hset(card_id, mapping=card)
    return await get_products_in_card(
        session=session, redis=redis, card_id=card_id
    )


async def get_product_quantity(session: AsyncSession, product_id: int) -> int:
    count_data = await ProductRepository.get_object_attrs_by_params(
        "count", session=session, data={"id": product_id}
    )
    return count_data.count
