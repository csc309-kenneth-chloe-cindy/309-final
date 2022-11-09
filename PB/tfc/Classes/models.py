from django.db import models
from accounts.models import User
# Create your models here.

class ClassOffering(models.Model):
    name = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=200, null=False)
    coach = models.CharField(max_length=200, null=False)
    times = models.CharField(max_length=200, null=False)
    capacity = models.PositiveIntegerField(max_length=200, null=False)
    studio = models.ForeignKey(to=Studio, on_delete=CASCADE, related_name='studio')

    def __str__(self):
        return self.name

class Keyword(models.Model):
    keyword = models.CharField(max_length=200, null=False)
    class_offering = models.ForeignKey(to=ClassOffering, on_delete=CASCADE, related_name='class_offering')

    def __str__(self):
        return self.name

class TimeInterval(models.Model):
    start_time = models.CharField(max_length=200, null=False)
    end_time = models.CharField(max_length=200, null=False)
    day_of_week = models.CharField(max_length=200, null=False)
    class_offering = models.ForeignKey(to=ClassOffering, on_delete=CASADE, related_name='class_offering')

    def __str__(self):
        return self.name

class ClassInstance(models.Model):
    date = models.CharField(max_length=200, null=False)
    capacity_count = models.PositiveIntegerField(default=0, null=False)
    class_offering = models.ForeignKey(to=ClassOffering, on_delete=CASCADE, related_name='class_offering')

    def __str__(self):
        return self.name

class UserEnroll(models.Model):
    class_instance = models.ForeignKey(to=ClassInstance, on_delete=CASCADE, related_name='class_instance')
    class_offering = models.ForeignKey(to=ClassOffering, on_delete=CASCADE, related_name='class_offering')
    user = models.ForeignKey(to=User, on_delete=CASCADE, related_name='users')

    def __str__(self):
        return self.name

class UserEnrollOffering(models.Model):
    class_offering = models.ForeignKey(to=ClassOffering, on_delete=CASCADE, related_name='class_offering')
    user = models.ForeignKey(to=User, on_delete=CASCADE, related_name='users')

    def __str__(self):
        return self.name
