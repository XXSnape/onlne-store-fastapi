from fastapi import APIRouter
from starlette.responses import Response

from core import SessionDep, UserIdDep
from orders.schemas.reviews import ReviewInSchema
from orders.services.review import write_review_on_product

router = APIRouter()


@router.post("/product/{product_id}/review")
async def write_review(
    session: SessionDep,
    product_id: int,
    user_id: UserIdDep,
    review_in: ReviewInSchema,
):
    await write_review_on_product(
        session=session,
        product_id=product_id,
        user_id=user_id,
        review_in=review_in,
    )
    return Response()
