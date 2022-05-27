from django.dispatch import Signal, receiver

reset_password_email = Signal()
reset_password_phone = Signal()
verify_email = Signal()
verify_phone = Signal()

@receiver(verify_email)
def verify_email_signal(sender, user, url, email, **kwargs):
    print(sender, user, url, email)
    print("Email Verfiication Signal")