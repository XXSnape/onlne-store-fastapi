from pydantic import BaseModel


class UserIsAuthenticatedSchema(BaseModel):
    pk: int | None = None
    is_authenticated: bool = False
    username: str | None = None
