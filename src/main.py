import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from core import db_helper
from frontend.routers import router as frontend_router

from products.admin import (
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
from products.routers.products import router as products_router
from users.admin import AvatarAdmin, UserAdmin
from sqladmin import Admin

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

app = FastAPI()
app.include_router(frontend_router)
app.include_router(users_router, prefix="/api")
app.include_router(profiles_router, prefix="/api")
app.include_router(products_router, prefix="/api")

app.mount("/static", StaticFiles(directory="frontend/static"))
app.mount("/order-detail/static/", StaticFiles(directory="frontend/static/"))
app.mount("/catalog/static/", StaticFiles(directory="frontend/static/"))
app.mount("/product/static/", StaticFiles(directory="frontend/static/"))
app.mount("/uploads", StaticFiles(directory="uploads/"))


@app.get("/api/products/limited")
async def products_limited():
    return [
        {
            "id": 123,
            "category": 55,
            "price": 500.67,
            "count": 12,
            "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
            "title": "video card",
            "description": "description of the product",
            "freeDelivery": True,
            "images": [{"src": "upload/1.png", "alt": "Image alt string"}],
            "tags": [{"id": 12, "name": "Gaming"}],
            "reviews": 5,
            "rating": 4.6,
        }
    ]


admin = Admin(app, db_helper.engine)
for view in views:
    admin.add_view(view)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
