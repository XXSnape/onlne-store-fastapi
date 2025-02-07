from json import loads
from typing import Annotated, TypeAlias

from fastapi import Body, Depends
from pydantic import BaseModel


class B(BaseModel):
    name: str
    username: str
    password: str


class StringOrModel:
    def __init__(self, schema: type[BaseModel]):
        self.schema = schema

    def __call__(self, data=Body()):
        print("data", data, type(data))
        if isinstance(data, (bytes, str)):
            return self.schema(**loads(data))
        if isinstance(data, dict):
            return self.schema(**data)


def get_credentials(credentials: Annotated[str | B, Body()]) -> dict[str, str]:
    print("cred", credentials, type(credentials))
    return loads(credentials)


CredentialsDep: TypeAlias = Annotated[
    dict[str, str | int], Depends(get_credentials)
]
