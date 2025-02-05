from pydantic import BaseModel
from pydantic.v1 import PositiveInt


class BasketInSchema(BaseModel):
    id: int
    count: int
