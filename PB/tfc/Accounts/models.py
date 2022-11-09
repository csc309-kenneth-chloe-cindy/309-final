from django.db import models

# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=200, null=False)
    last_name = models.CharField(max_length=200, null=False)
    email = models.CharField(max_length=200, null=False)
    avatar = models.ImageField()
    phone_number = models.CharField(max_length=200, null=False)