from typing import Annotated, TypeAlias

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper

SessionDep: TypeAlias = Annotated[
    AsyncSession, Depends(db_helper.get_async_session)
]
