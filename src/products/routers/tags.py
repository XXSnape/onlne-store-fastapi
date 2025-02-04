from typing import Annotated

from fastapi import APIRouter, Query

from core import SessionDep
from products.services.tags import get_tags_by_category_id

router = APIRouter()


@router.get("/tags")
async def get_tags(
    session: SessionDep,
    category_id: Annotated[int | None, Query(alias="category")] = None,
):
    return await get_tags_by_category_id(
        session=session, category_id=category_id
    )
