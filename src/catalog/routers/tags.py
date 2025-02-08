from typing import Annotated

from fastapi import APIRouter, Query

from catalog.schemas.tags import TagSchema
from core import SessionDep
from catalog.services.tags import get_tags_by_category_id

router = APIRouter()


@router.get("/tags", response_model=list[TagSchema])
async def get_tags(
    session: SessionDep,
    category_id: Annotated[int | None, Query(alias="category")] = None,
):
    return await get_tags_by_category_id(
        session=session, category_id=category_id
    )
