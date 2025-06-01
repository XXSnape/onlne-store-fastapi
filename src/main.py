import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin
from starlette.staticfiles import StaticFiles

from catalog.admin import (
    CategoryAdmin,
    CategoryImageAdmin,
    ProductAdmin,
    ProductImageAdmin,
    ReviewAdmin,
    SaleAdmin,
    SpecificationAdmin,
    SpecificationProductAdmin,
    TagAdmin,
    TagCategoryAdmin,
)
from catalog.routers import router as products_router
from core import db_helper, settings
from core.admin.auth import AdminAuth
from core.admin.superuser import create_admin_if_not_exists
from frontend.routers import router as frontend_router
from orders.admin import OrderAdmin, OrderProductAdmin
from orders.routers import router as orders_router
from users.admin import AvatarAdmin, UserAdmin
from users.routers.auth import router as users_router
from users.routers.profile import router as profiles_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(settings.redis.url)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
    await redis.close()


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
    OrderAdmin,
    OrderProductAdmin,
]

app = FastAPI(lifespan=lifespan)
app.include_router(frontend_router)
app.include_router(users_router, prefix="/api")
app.include_router(profiles_router, prefix="/api")
app.include_router(products_router, prefix="/api")
app.include_router(orders_router, prefix="/api")

FRONTEND_DIR = Path(__file__).resolve().parent / "frontend" / "static"

app.mount("/static", StaticFiles(directory=FRONTEND_DIR))
app.mount("/order-detail/static/", StaticFiles(directory=FRONTEND_DIR))
app.mount("/catalog/static/", StaticFiles(directory=FRONTEND_DIR))
app.mount("/product/static/", StaticFiles(directory=FRONTEND_DIR))
app.mount("/uploads", StaticFiles(directory="uploads/"))
app.mount("/product/uploads", StaticFiles(directory="uploads/"))
app.mount("/catalog/uploads", StaticFiles(directory="uploads/"))

authentication_backend = AdminAuth(secret_key=settings.app.session_key)
admin = Admin(
    app, db_helper.engine, authentication_backend=authentication_backend
)
for view in views:
    admin.add_view(view)


if __name__ == "__main__":
    asyncio.run(create_admin_if_not_exists())
    uvicorn.run("main:app", reload=True, host="0.0.0.0")
