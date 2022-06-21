from django.contrib import admin
from .models import Store, StoreSetting, Order
# Register your models here.
admin.site.register(Store)
admin.site.register(StoreSetting)
admin.site.register(Order)
