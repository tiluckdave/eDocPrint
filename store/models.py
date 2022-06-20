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
        return self.Store_name + " - " + self.Store_operator
    
class StoreSetting(models.Model):
    store = models.OneToOneField(Store, on_delete=models.CASCADE)
    bnw_one_side_rate = models.DecimalField(max_digits=10, decimal_places=2, default=2.00)
    bnw_two_side_rate = models.DecimalField(max_digits=10, decimal_places=2, default=3.00)
    color_one_side_rate = models.DecimalField(max_digits=10, decimal_places=2, default=5.00)
    color_two_side_rate = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    photo_4x6_rate = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    photo_A4_rate = models.DecimalField(max_digits=10, decimal_places=2, default=20.00)
    
    def __str__(self):
        return self.store
    
    
    
    