from django.urls import path
from . import  views


urlpatterns = [
    path("", views.index, name="index"),
    path("documents", views.yourdocs, name="yourdocs"),
    path("settings", views.settings, name="settings"),
    path("add-address/", views.addAddress, name="addAddress"),
    path("delete-address/<int:id>", views.deleteAddr, name="deleteAddr"),
    path("delete-document/<int:id>", views.deleteDoc, name="deleteDoc"),
    path('config/', views.stripe_config),  # new
    path('create-checkout-session/<str:rate>/<str:order_id>', views.create_checkout_session, name="ccs"), # 
    path('success', views.SuccessView), # new
    path('cancelled/', views.CancelledView), # new
    path('getRates', views.getRates, name="getRates"), # new
]