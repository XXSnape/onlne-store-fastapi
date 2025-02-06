from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from catalog.schemas.products import ProductGeneralSchema
from core import SessionDep, UserIdDep
from orders.services.order import add_products_to_new_order

router = APIRouter()


@router.post("/orders")
async def create_order(
    session: SessionDep,
    user_id: UserIdDep,
    products: list[ProductGeneralSchema],
):
    order_id = await add_products_to_new_order(
        session=session,
        user_id=user_id,
        products=products,
    )
    return {"orderId": order_id}
