from fastapi import APIRouter, Depends
from starlette.responses import Response

from catalog.schemas.products import ProductGeneralSchema
from core import SessionDep, UserIdDep
from core.dependencies.user_by_cookie import get_user_id
from orders.schemas.orders import OrderIdOutSchema, OrderInSchema, OrdersSchema
from orders.services.orders import (
    add_details_to_order,
    add_products_to_new_order,
    get_user_order,
    get_user_orders,
)

router = APIRouter(tags=['orders'])


@router.post("/orders", response_model=OrderIdOutSchema)
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


@router.post("/orders/{order_id}", dependencies=[Depends(get_user_id)])
async def confirm_order(
    order_id: int,
    session: SessionDep,
    user_id: UserIdDep,
    order_details: OrderInSchema,
):
    await add_details_to_order(
        order_id=order_id,
        session=session,
        user_id=user_id,
        order_details=order_details,
    )
    return Response()


@router.get("/orders", response_model=list[OrdersSchema])
async def get_orders(
    session: SessionDep,
    user_id: UserIdDep,
):
    return await get_user_orders(session=session, user_id=user_id)


@router.get("/orders/{order_id}", response_model=OrdersSchema)
async def get_order(session: SessionDep, user_id: UserIdDep, order_id: int):
    return await get_user_order(
        session=session,
        user_id=user_id,
        order_id=order_id,
    )
