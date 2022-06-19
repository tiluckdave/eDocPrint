from django.db import models
from django.contrib.auth.model import User

# Create your models here.
class Store(models.Model):
    account = one_to_one_field(User, on_delete=models.CASCADE)
    Store_name = models.CharField(max_length=100)
    store_address = models.CharField(max_length=1000)
    std_rate = models.IntegerField()
    color_rate = models.IntegerField()
    photo_rate = models.IntegerField()
    