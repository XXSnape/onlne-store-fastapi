from fastapi import HTTPException
from starlette import status

incorrect_extension = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail="Файл должен быть картинкой",
)
