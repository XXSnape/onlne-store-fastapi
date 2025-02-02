from pydantic import BaseModel, Field
from typing import Annotated


class AvatarSchema(BaseModel):
    src: str
    alt: str


class ProfileSchema(BaseModel):
    fullname: str
    email: str
    phone: str
    avatar: Annotated[AvatarSchema | None, Field(default=None)]
