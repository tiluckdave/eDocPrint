from django.db import models
from django.db.models.fields import CharField
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _
from .constants import PaymentStatus
import uuid

key = os.getenv('PIN_KEY')

fernet = Fernet(key)

# Create your models here.
load_dotenv()
class SecurePin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pin = models.CharField(max_length=1000)

    def __str__(self):
        return self.user.username
    
    def save(self):
        self.pin = fernet.encrypt(self.pin.decode('utf-8').encode())
        super().save()


def get_file_path(instance, filename):
    name = filename.split('.')[0]
    ext = filename.split('.')[-1]
    filename = "%s-%s.%s" % (name, uuid.uuid4(), ext)
    return os.path.join('documents', filename)

class Document(models.Model):
    name = models.CharField(max_length=100)
    document = models.FileField(upload_to=get_file_path)
    pages = models.IntegerField(default=0)
    prize = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
class Order(models.Model):
    name = CharField(_("Customer Name"), max_length=254, blank=False, null=False)
    amount = models.FloatField(_("Amount"), null=False, blank=False)
    status = CharField(
        _("Payment Status"),
        default=PaymentStatus.PENDING,
        max_length=254,
        blank=False,
        null=False,
    )
    provider_order_id = models.CharField(
        _("Order ID"), max_length=40, null=False, blank=False
    )
    payment_id = models.CharField(
        _("Payment ID"), max_length=36, null=False, blank=False
    )
    signature_id = models.CharField(
        _("Signature ID"), max_length=128, null=False, blank=False
    )

    def __str__(self):
        return f"{self.id}-{self.name}-{self.status}"