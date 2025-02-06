from pydantic import BaseModel
from datetime import datetime


class ReviewSchema(BaseModel):
    author: str
    email: str
    text: str
    rate: int
    date: datetime
