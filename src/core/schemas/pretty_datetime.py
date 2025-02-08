from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, PlainSerializer


class DateSchema(BaseModel):
    date: Annotated[
        datetime, PlainSerializer(lambda d: d.strftime("%Y-%m-%d %H:%M:%S"))
    ]
