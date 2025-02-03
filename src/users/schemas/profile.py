from pydantic import BaseModel, Field, AliasChoices
from typing import Annotated

from core import ImageSchema


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


class ProfileSchema(ProfileInSchema):
    avatar: Annotated[ImageSchema | None, Field(default=None)]
