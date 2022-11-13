from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class TFCUser(AbstractUser):
    email = models.EmailField(null=False)
    username = models.CharField(null=False)
    password = models.CharField(null=False)
    first_name = models.CharField(max_length=200, null=False)
    last_name = models.CharField(max_length=200, null=False)
    phone_number = models.CharField(max_length=200, null=False)
    avatar = models.ImageField()

    def __str__(self):
        return self.username