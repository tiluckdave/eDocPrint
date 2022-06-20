from django.urls import path
from . import  views


urlpatterns = [
    path("dashboard", views.dashboard, name="dashboard"),
    path("register-store", views.registerStore, name="registerStore"),
    path("update-store-details", views.updateStoreDetails, name="updateStoreDetails"),
    path("toggle-store", views.toggleStore, name="toggleStore"),
    path("orders", views.orders, name="orders"),
]