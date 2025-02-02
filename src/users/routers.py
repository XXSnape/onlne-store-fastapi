from typing import Annotated

from fastapi import APIRouter, Query
from .schemas.sign_up import SignUpSchema

router = APIRouter()


@router.post("/sign-up")
def sign_up(credentials: Annotated[SignUpSchema, Query()]):
    pass
