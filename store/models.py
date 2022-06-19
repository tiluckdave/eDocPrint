from django.db import models
from django.contrib.auth.models import User
from main.models import Address

# Create your models here.
class Store(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Store_name = models.CharField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    Store_email = models.EmailField(max_length=254)
    Store_phone = models.CharField(max_length=10)
    Store_operator = models.CharField(max_length=100)
    
    def __str__(self):
        return self.Store_name + " " + self.Store_email + " " + self.Store_phone + " " + self.Store_operator
    
class StoreSetting(models.Model):
    store = models.OneToOneField(Store, on_delete=models.CASCADE)
    
    