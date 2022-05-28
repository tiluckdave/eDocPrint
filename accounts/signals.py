from django.dispatch import Signal, receiver
from django.conf import settings
from twilio.rest import Client
from django.core.mail import send_mail

reset_password_email = Signal()
reset_password_phone = Signal()
verify_email = Signal()
verify_phone = Signal()

@receiver(verify_email)
def verify_email_signal(sender, user, url, email, **kwargs):
    print(sender, user, url, email)
    subject = 'welcome to eDocPrint'
    message = f'Hi {user.first_name} {user.last_name}, thank you for registering on eDocPrint.\nClick on the link below to verify your email!\nhttp://127.0.0.1:8000{url}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email,]
    send_mail( subject, message, email_from, recipient_list )

@receiver(verify_phone)
def verify_phone_signal(sender, user, url, phone, **kwargs):
    account_sid = 'AC6f9d591b2d43a35b9aee73ed050fc401'
    auth_token = 'c4c7f97624dc5f6b90fd6745d835c3b8'
    client = Client(account_sid, auth_token)
    body = f'Welcome to eDocPrint,\nHi {user.first_name} {user.last_name}, thank you for registering on eDocPrint.\nClick on the link below to verify your phone!\nhttp://127.0.0.1:8000{url}'
    message = client.messages.create(body=body, from_='+12722826951',to=phone )