from django.db import models
from django.db.models.fields import CharField
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv
import uuid

key = os.getenv('PIN_KEY')

fernet = Fernet(key)

# Create your models here.
load_dotenv()

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    area = models.CharField(max_length=100, default='')
    distrcit = models.CharField(max_length=100, default="")
    state = models.CharField(max_length=100, default="")
    country = models.CharField(max_length=100, default="")
    pincode = models.CharField(max_length=6, default="")
    
    def __str__(self):
        return self.area + ", " + self.distrcit + ", " + self.state + ", " + self.country + ", " + self.pincode
    

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
    

    