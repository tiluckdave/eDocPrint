from django.urls import path
from . import  views


urlpatterns = [
    path("register-store", views.registerStore, name="registerStore"),
    path("toggle-store", views.toggleStore, name="toggleStore"),
]