from typing import Annotated

from pydantic import BaseModel, Field


class SignUpSchema(BaseModel):
    name: Annotated[str, Field(pattern=r"\w+ \w+$")]
    username: Annotated[str, Field(max_length=32, min_length=1)]
    password: Annotated[str, Field(min_length=5)]
