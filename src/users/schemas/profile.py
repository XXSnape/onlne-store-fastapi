from typing import Annotated

from pydantic import AliasChoices, BaseModel, Field

from core import ImageSchema


class ProfileInSchema(BaseModel):
    fullname: Annotated[
        str,
        Field(
            validation_alias=AliasChoices("fullname", "fullName"),
            serialization_alias="fullName",
            pattern=r"^\w+ \w+$",
        ),
    ]
    email: str
    phone: str


class ProfileSchema(ProfileInSchema):
    avatar: Annotated[ImageSchema | None, Field(default=None)]
