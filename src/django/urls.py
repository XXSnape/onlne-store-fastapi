from src.django.urls import path
from src.django.views import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="frontend2/index.html")),
    path("about/", TemplateView.as_view(template_name="frontend2/about.html")),
    path("account/", TemplateView.as_view(template_name="frontend2/account.html")),
    path("cart/", TemplateView.as_view(template_name="frontend2/cart.html")),
    path("catalog/", TemplateView.as_view(template_name="frontend2/catalog.html")),
    path(
        "catalog/<int:id>/",
        TemplateView.as_view(template_name="frontend2/catalog.html"),
    ),
    path(
        "history-order/",
        TemplateView.as_view(template_name="frontend2/historyorder.html"),
    ),
    path(
        "order-detail/<int:id>/",
        TemplateView.as_view(template_name="frontend2/oneorder.html"),
    ),
    path(
        "orders/<int:id>/", TemplateView.as_view(template_name="frontend2/order.html")
    ),
    path(
        "payment/<int:id>/",
        TemplateView.as_view(template_name="frontend2/payment.html"),
    ),
    path(
        "payment-someone/",
        TemplateView.as_view(template_name="frontend2/paymentsomeone.html"),
    ),
    path(
        "product/<int:id>/",
        TemplateView.as_view(template_name="frontend2/product.html"),
    ),
    path("profile/", TemplateView.as_view(template_name="frontend2/profile.html")),
    path(
        "progress-payment/",
        TemplateView.as_view(template_name="frontend2/progressPayment.html"),
    ),
    path("sale/", TemplateView.as_view(template_name="frontend2/sale.html")),
    path("sign-in/", TemplateView.as_view(template_name="frontend2/signIn.html")),
    path("sign-up/", TemplateView.as_view(template_name="frontend2/signUp.html")),
]
