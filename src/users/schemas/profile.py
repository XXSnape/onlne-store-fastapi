from pydantic import BaseModel, Field, AliasChoices
from typing import Annotated


class ProfileInSchema(BaseModel):
    fullname: Annotated[
        str,
        Field(
            validation_alias=AliasChoices("fullname", "fullName"),
            serialization_alias="fullName",
        ),
    ]
    email: str
    phone: str


class AvatarSchema(BaseModel):
    src: str
    alt: str


class ProfileSchema(ProfileInSchema):
    avatar: Annotated[AvatarSchema | None, Field(default=None)]
