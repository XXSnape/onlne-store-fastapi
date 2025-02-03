from pydantic import BaseModel


class ImageSchema(BaseModel):
    src: str
    alt: str
