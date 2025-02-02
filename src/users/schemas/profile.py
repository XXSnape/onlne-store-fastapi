from pydantic import BaseModel, Field
from typing import Annotated


class ProfileGeneralSchema(BaseModel):
    email: str
    phone: str


class ProfileInSchema(ProfileGeneralSchema):
    fullname: Annotated[str, Field(validation_alias="fullName")]


class AvatarSchema(BaseModel):
    src: str
    alt: str


class ProfileSchema(ProfileGeneralSchema):
    fullname: Annotated[str, Field(serialization_alias="fullName")]
    avatar: Annotated[AvatarSchema | None, Field(default=None)]
