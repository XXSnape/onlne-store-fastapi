from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from catalog.schemas.products import ProductGeneralSchema
from core import SessionDep, UserIdDep

router = APIRouter()


@router.post("/orders")
async def create_order(
    session: SessionDep,
    user_id: UserIdDep,
    products: list[ProductGeneralSchema],
):
    print(products)

    pass
