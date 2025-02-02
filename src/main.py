import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from frontend.routers import router as frontend_router

app = FastAPI()
app.include_router(frontend_router)

app.mount("/static", StaticFiles(directory="src/frontend/static"))
app.mount("/order-detail/static/", StaticFiles(directory="src/frontend/static/"))
app.mount("/catalog/static/", StaticFiles(directory="src/frontend/static/"))
app.mount("/upload", StaticFiles(directory="src/upload/"))

@app.get('/api/products/limited')
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
    "images": [
      {
        "src": "upload/1.png",
        "alt": "Image alt string"
      }
    ],
    "tags": [
      {
        "id": 12,
        "name": "Gaming"
      }
    ],
    "reviews": 5,
    "rating": 4.6
  }
]



if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
