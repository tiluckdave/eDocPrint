from django.db import models
from django.contrib.auth.models import User
from main.models import Address, Document
import datetime

# Create your models here.
class Store(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Store_name = models.CharField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    Store_email = models.EmailField(max_length=254)
    Store_phone = models.CharField(max_length=10)
    Store_operator = models.CharField(max_length=100)
    
    def __str__(self):
        return self.Store_name + " - " + self.address.__str__()
    
class StoreSetting(models.Model):
    store = models.OneToOneField(Store, on_delete=models.CASCADE)
    bnw_one_side_rate = models.DecimalField(max_digits=10, decimal_places=2, default=2.00)
    bnw_two_side_rate = models.DecimalField(max_digits=10, decimal_places=2, default=3.00)
    color_one_side_rate = models.DecimalField(max_digits=10, decimal_places=2, default=5.00)
    color_two_side_rate = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    photo_4x6_rate = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    photo_A4_rate = models.DecimalField(max_digits=10, decimal_places=2, default=20.00)
    
    def get_rate(self, pt):
        if pt == "bo":
            return self.bnw_one_side_rate
        elif pt == "bt":
            return self.bnw_two_side_rate/2
        elif pt == "co":
            return self.color_one_side_rate
        elif pt == "ct":
            return self.color_two_side_rate/2
        elif pt == "ps":
            return self.photo_4x6_rate
        elif pt == "pl":
            return self.photo_A4_rate
    
    def __str__(self):
        return self.store
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, blank=True, null=True)
    upload = models.FileField(upload_to='documents/', blank=True, null=True)
    print_type = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    tostore_rate = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    payment_mode = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
        
    
    def __str__(self):
        return self.user.username + " - " + self.store.Store_name + " - " + self.document.name
    
    
    
    