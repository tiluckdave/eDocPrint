from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

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

class Document(models.Model):
    name = models.CharField(max_length=100)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)