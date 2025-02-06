from fastapi import HTTPException, status

not_found = HTTPException(status_code=status.HTTP_404_NOT_FOUND)
