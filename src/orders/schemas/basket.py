from pydantic import BaseModel


class BasketInSchema(BaseModel):
    id: int
    count: int
