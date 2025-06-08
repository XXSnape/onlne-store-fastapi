from fastapi import HTTPException, status

too_many_products = HTTPException(
    detail="Нет столько товара в наличии",
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
)
there_are_no_items_in_cart = HTTPException(
    detail="В корзине нет этого товара",
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
)