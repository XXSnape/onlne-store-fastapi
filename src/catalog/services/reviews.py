from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from catalog.database.repositories.product import ProductRepository
from catalog.database.repositories.review import ReviewRepository
from catalog.schemas.reviews import ReviewInSchema, ReviewSchema


async def write_review_on_product(
    session: AsyncSession,
    user_id: int,
    product_id: int,
    review_in: ReviewInSchema,
):
    result = await ProductRepository.is_there_purchase(
        session=session,
        user_id=user_id,
        product_id=product_id,
    )
    if result is False:
        raise HTTPException(
            detail="Товар не был куплен",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    await ReviewRepository.create_object(
        session=session,
        data={
            "user_id": user_id,
            "product_id": product_id,
            **review_in.model_dump(),
        },
    )
    reviews = await ProductRepository.get_product_reviews(
        session=session, product_id=product_id
    )
    return [
        ReviewSchema.model_validate(review, from_attributes=True)
        for review in reviews
    ]
