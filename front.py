from starlette.requests import Request
from starlette.responses import HTMLResponse
from fastapi import APIRouter
from starlette.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


router = APIRouter()
templates = Jinja2Templates(
    directory="frontend/templates/",
)

class A:
    is_authenticated = True


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "user": A()})


@router.get("about/")
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request, "user": A()})


@router.get("account/")
async def account(request: Request):
    return templates.TemplateResponse("account.html", {"request": request, "user": A()})


@router.get("cart/")
async def cart(request: Request):
    return templates.TemplateResponse("cart.html", {"request": request, "user": A()})


@router.get("catalog/")
async def catalog(request: Request):
    return templates.TemplateResponse("catalog.html", {"request": request, "user": A()})


@router.get("catalog/{id}/")
async def about(request: Request):
    return templates.TemplateResponse("catalog.html", {"request": request, "user": A()})


@router.get("history-order/")
async def history(request: Request):
    return templates.TemplateResponse(
        "historyorder.html", {"request": request, "user": A()}
    )


@router.get("order-detail/{id}/")
async def about(request: Request):
    return templates.TemplateResponse("catalog.html", {"request": request, "user": A()})


@router.get("about/")
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request, "user": A()})


@router.get("about/")
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request, "user": A()})
