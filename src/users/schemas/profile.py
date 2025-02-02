from pydantic import BaseModel, Field
from sqlalchemy.sql.annotation import Annotated


class AvatarSchema(BaseModel):
    src: str
    alt: str


class ProfileSchema(BaseModel):
    fullname: str
    email: str
    phone: str
    avatar: Annotated[AvatarSchema | dict, Field(default_factory=dict)]
