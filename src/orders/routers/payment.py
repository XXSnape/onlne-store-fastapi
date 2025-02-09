from fastapi import APIRouter
from starlette.responses import Response

from core import SessionDep, UserIdDep
from orders.schemas.payment import PaymentInSchema
from orders.services.orders import pay_order

router = APIRouter(tags=['payment'])


@router.post("/payment/{order_id}")
async def pay_for_order(
    session: SessionDep,
    payment_id: PaymentInSchema,
    user_id: UserIdDep,
    order_id: int,
):
    await pay_order(session=session, user_id=user_id, order_id=order_id)
    return Response()
