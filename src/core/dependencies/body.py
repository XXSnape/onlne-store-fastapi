from json import loads

from fastapi import Body, HTTPException, status
from pydantic import BaseModel, ValidationError

from core import logger


class SchemaDep:
    def __init__(self, schema: type[BaseModel]):
        self.schema = schema

    def __call__(self, data=Body()):
        data_in = {}
        if isinstance(data, (bytes, str)):
            data_in = loads(data)
        elif isinstance(data, dict):
            data_in = data
        try:
            return self.schema(**data_in)
        except ValidationError as e:
            logger.exception('Невалидные данные из запроса', extra={'data': data})
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=e.errors(),
            )
