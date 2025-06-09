from pydantic import BaseModel


class SpecificationSchema(BaseModel):
    name: str
    value: str
