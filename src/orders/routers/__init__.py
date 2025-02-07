from fastapi import APIRouter

from .orders import router as orders_router
from .payment import router as payment_router

router = APIRouter()
router.include_router(orders_router)
router.include_router(payment_router)
