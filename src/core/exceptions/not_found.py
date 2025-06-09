from fastapi import HTTPException, status

not_found = HTTPException(status_code=status.HTTP_404_NOT_FOUND)
no_product_with_these_parameters_was_found = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
)
