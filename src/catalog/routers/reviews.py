from fastapi import APIRouter

from catalog.schemas.reviews import ReviewInSchema, ReviewSchema
from catalog.services.reviews import write_review_on_product
from core import SessionDep, UserIdDep

router = APIRouter()


@router.post(
    "/product/{product_id}/reviews", response_model=list[ReviewSchema]
)
async def write_review(
    session: SessionDep,
    product_id: int,
    user_id: UserIdDep,
    review_in: ReviewInSchema,
):
    return await write_review_on_product(
        session=session,
        product_id=product_id,
        user_id=user_id,
        review_in=review_in,
    )
    # return Response()
