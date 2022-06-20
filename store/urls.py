from django.urls import path
from . import  views


urlpatterns = [
    path("dashboard", views.dashboard, name="dashboard"),
    path("register-store", views.registerStore, name="registerStore"),
    path("update-store-details", views.updateStoreDetails, name="updateStoreDetails"),
    path("update-store-rates", views.updateStoreRates, name="updateStoreRates"),
    path("toggle-store", views.toggleStore, name="toggleStore"),
    path("orders", views.orders, name="orders"),
    path("create-order", views.createOrder, name="createOrder"),
    path("delete-order/<int:id>", views.deleteOrder, name="deleteOrder"),
    path("paid-order/<int:id>", views.paidOrder, name="paidOrder"),
]