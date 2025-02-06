from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from catalog.database.repositories.review import ReviewRepository
from orders.database.repositories.order import OrderProductRepository
from orders.schemas.reviews import ReviewInSchema


async def write_review_on_product(
    session: AsyncSession,
    user_id: int,
    product_id: int,
    review_in: ReviewInSchema,
):
    result = await OrderProductRepository.is_there_purchase(
        session=session,
        user_id=user_id,
        product_id=product_id,
    )
    if result is False:
        raise HTTPException(
            detail="Товар не был куплен", status_code=status.HTTP_403_FORBIDDEN
        )
    await ReviewRepository.create_object(
        session=session,
        data={
            "user_id": user_id,
            "product_id": product_id,
            **review_in.model_dump(),
        },
    )
