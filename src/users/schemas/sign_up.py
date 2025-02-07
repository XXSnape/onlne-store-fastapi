from typing import Annotated

from pydantic import BaseModel, Field, PlainSerializer

from users.utils.auth import get_hashed_password


class SignUpSchema(BaseModel):
    fullname: Annotated[
        str,
        Field(
            pattern=r"^\w+ \w+$",
            validation_alias="name",
        ),
    ]
    username: Annotated[str, Field(max_length=32, min_length=1)]
    password: Annotated[
        str,
        Field(min_length=5),
        PlainSerializer(get_hashed_password, return_type=bytes),
    ]
