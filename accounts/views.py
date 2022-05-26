from django.shortcuts import render
from django.contrib.auth import get_user_model
from django_email_verification import send_email


def signup(request, username, email, password):
    user = get_user_model().objects.create(username=username, password=password, email=email)
    user.is_active = False  
    send_email(user)
    return render(request, "accounts/signup.html")