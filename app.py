import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from front import router as frontend_router

app = FastAPI()
app.include_router(frontend_router)

app.mount("/static", StaticFiles(directory="frontend/static/"))


if __name__ == '__main__':
    uvicorn.run("app:app", reload=True)
