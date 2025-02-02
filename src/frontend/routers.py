from starlette.requests import Request
from starlette.responses import HTMLResponse
from fastapi import APIRouter
from starlette.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(
    directory="src/frontend/templates/",
)


class A:
    is_authenticated = False


@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "user": A()}
    )


@router.get("/about")
async def about(request: Request):
    return templates.TemplateResponse(
        "about.html", {"request": request, "user": A()}
    )


@router.get("/account")
async def account(request: Request):
    return templates.TemplateResponse(
        "account.html", {"request": request, "user": A()}
    )


@router.get("/cart")
async def cart(request: Request):
    return templates.TemplateResponse(
        "cart.html", {"request": request, "user": A()}
    )


@router.get("/catalog", response_class=HTMLResponse)
async def catalog(request: Request):
    return templates.TemplateResponse(
        "catalog.html", {"request": request, "user": A()}
    )


@router.get("/catalog/{id}")
async def catalog_id(request: Request):
    return templates.TemplateResponse(
        "catalog.html", {"request": request, "user": A()}
    )


@router.get("/history-order")
async def history_order(request: Request):
    return templates.TemplateResponse(
        "historyorder.html", {"request": request, "user": A()}
    )


@router.get("/order-detail/{id}")
async def order_detail(request: Request):
    return templates.TemplateResponse(
        "oneorder.html", {"request": request, "user": A()}
    )


@router.get("/orders/<int:id>")
async def orders_id(request: Request):
    return templates.TemplateResponse(
        "order.html", {"request": request, "user": A()}
    )


@router.get("/payment/{id}")
async def payment_id(request: Request):
    return templates.TemplateResponse(
        "payment.html", {"request": request, "user": A()}
    )


@router.get("/payment-someone")
async def payment_someone(request: Request):
    return templates.TemplateResponse(
        "paymentsomeone.html", {"request": request, "user": A()}
    )


@router.get("/product/<int:id>")
async def product_id(request: Request):
    return templates.TemplateResponse(
        "product.html", {"request": request, "user": A()}
    )


@router.get("/profile")
async def profile(request: Request):
    return templates.TemplateResponse(
        "profile.html", {"request": request, "user": A()}
    )


@router.get("/progress-payment")
async def progress_payment(request: Request):
    return templates.TemplateResponse(
        "progressPayment.html", {"request": request, "user": A()}
    )


@router.get("/sale")
async def sale(request: Request):
    return templates.TemplateResponse(
        "sale.html", {"request": request, "user": A()}
    )


@router.get("/sign-in")
async def sign_in(request: Request):
    return templates.TemplateResponse(
        "signIn.html", {"request": request, "user": A()}
    )


@router.get("/sign-up")
async def sign_up(request: Request):
    return templates.TemplateResponse(
        "signUp.html", {"request": request, "user": A()}
    )
