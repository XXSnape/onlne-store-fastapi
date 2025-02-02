from pydantic import BaseModel


class UserIsAuthenticatedSchema(BaseModel):
    is_authenticated: bool = False
    username: str | None = None
