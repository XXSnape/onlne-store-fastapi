from typing import Annotated

from pydantic import BaseModel, Field
from datetime import datetime


class ReviewInSchema(BaseModel):
    text: str
    rate: Annotated[int, Field(ge=1, le=5)]


class ReviewSchema(ReviewInSchema):
    author: str
    email: str
    date: datetime
