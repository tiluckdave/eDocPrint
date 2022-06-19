from django.contrib import admin
from .models import Document, SecurePin, Address
# Register your models here.
admin.site.register(Document)
admin.site.register(SecurePin)
admin.site.register(Address)
