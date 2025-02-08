from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, PlainSerializer

datetime_serializer = PlainSerializer(
    lambda d: d.strftime("%Y-%m-%d %H:%M:%S")
)


class DateSchema(BaseModel):
    date: Annotated[datetime, datetime_serializer]
