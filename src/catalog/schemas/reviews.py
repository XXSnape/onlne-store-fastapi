from typing import Annotated

from pydantic import BaseModel, Field

from core import DateSchema


class ReviewInSchema(BaseModel):
    text: str
    rate: Annotated[int, Field(ge=1, le=5)]


class ReviewSchema(ReviewInSchema, DateSchema):
    author: str
    email: str
