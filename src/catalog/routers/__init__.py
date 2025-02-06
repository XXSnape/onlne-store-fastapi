from fastapi import APIRouter
from .products import router as products_router
from .tags import router as tags_router
from .basket import router as basket_router

router = APIRouter()

router.include_router(products_router)
router.include_router(tags_router)
router.include_router(basket_router)
