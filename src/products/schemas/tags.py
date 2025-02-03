from pydantic import BaseModel


class TagSchema(BaseModel):
    id: int
    name: str
