import uvicorn
from starlette.staticfiles import StaticFiles

from core import db_helper, settings
from frontend.routers import router as frontend_router

from catalog.admin import (
    CategoryAdmin,
    CategoryImageAdmin,
    TagAdmin,
    TagCategoryAdmin,
    ProductAdmin,
    ProductImageAdmin,
    SpecificationAdmin,
    SpecificationProductAdmin,
    ReviewAdmin,
    SaleAdmin,
)
from users.routers.auth import router as users_router
from users.routers.profile import router as profiles_router
from catalog.routers import router as products_router
from orders.routers import router as orders_router
from users.admin import AvatarAdmin, UserAdmin
from sqladmin import Admin
from redis import asyncio as aioredis

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(settings.redis.url)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


views = [
    CategoryAdmin,
    CategoryImageAdmin,
    TagAdmin,
    TagCategoryAdmin,
    ProductAdmin,
    ProductImageAdmin,
    SpecificationAdmin,
    SpecificationProductAdmin,
    ReviewAdmin,
    AvatarAdmin,
    UserAdmin,
    SaleAdmin,
]

app = FastAPI(lifespan=lifespan)
app.include_router(frontend_router)
app.include_router(users_router, prefix="/api")
app.include_router(profiles_router, prefix="/api")
app.include_router(products_router, prefix="/api")

app.mount("/static", StaticFiles(directory="frontend/static"))
app.mount("/order-detail/static/", StaticFiles(directory="frontend/static/"))
app.mount("/catalog/static/", StaticFiles(directory="frontend/static/"))
app.mount("/product/static/", StaticFiles(directory="frontend/static/"))
app.mount("/uploads", StaticFiles(directory="uploads/"))
app.mount("/product/uploads", StaticFiles(directory="uploads/"))


admin = Admin(app, db_helper.engine)
for view in views:
    admin.add_view(view)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
