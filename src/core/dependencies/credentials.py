from json import loads
from typing import Annotated, TypeAlias

from fastapi import Body, Depends


def get_credentials(credentials: Annotated[str, Body()]) -> dict[str, str]:
    return loads(credentials)


CredentialsDep: TypeAlias = Annotated[
    dict[str, str | int], Depends(get_credentials)
]
