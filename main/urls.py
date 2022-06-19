from django.urls import path
from . import  views


urlpatterns = [
    path("", views.index, name="index"),
    path("documents", views.yourdocs, name="yourdocs"),
    path("settings", views.settings, name="settings"),
    path("payment/", views.order_payment, name="payment"),
    path("add-address/", views.addAddress, name="addAddress"),
    path("delete-address/<int:id>", views.deleteAddr, name="deleteAddr"),
]