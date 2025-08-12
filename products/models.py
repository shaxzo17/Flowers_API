from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Flower(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=9 , decimal_places=2 , blank=True , null=True)
    image = models.ImageField(upload_to='flowers/' , blank=True , null=True)

    def __str__(self):
        return self.name

# class CustomUser(AbstractUser):
#     address = models.CharField(max_length=255, blank=True, null=True)
#
#     def __str__(self):
#         return self.username
