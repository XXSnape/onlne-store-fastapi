from fastapi import HTTPException, status

unauthorized_error = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неверный логин или пароль",
)
