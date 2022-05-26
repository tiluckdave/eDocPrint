from django.urls import path
from . import views

urlpatterns = [
    path('signup/<username>/<email>/<password>', views.signup),
]
