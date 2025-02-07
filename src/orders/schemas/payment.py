from typing import Annotated

from pydantic import BaseModel, Field


class PaymentInSchema(BaseModel):
    number: Annotated[str, Field(pattern=r"^\d{16}$")]
    name: str
    month: Annotated[int, Field(ge=1, le=12)]
    year: Annotated[int, Field(ge=2000, le=2100)]
    code: Annotated[int, Field(ge=100, le=999)]
