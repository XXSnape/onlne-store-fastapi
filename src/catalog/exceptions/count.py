from fastapi import HTTPException, status

too_many_products = HTTPException(
    detail="Нет столько товара в наличии",
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
)
