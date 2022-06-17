from django.urls import path
from . import  views


urlpatterns = [
    path("", views.index, name="index"),
    path("documents", views.yourdocs, name="yourdocs"),
    path("settings", views.settings, name="settings"),
    path("payment/", views.order_payment, name="payment"),
]