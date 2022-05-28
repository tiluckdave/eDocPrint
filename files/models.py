from django.db import models

# Create your models here.
class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    otp = models.IntegerField(max_length=4)
    key = models.CharField(max_length=255)

    def __str__(self):
        return self.name