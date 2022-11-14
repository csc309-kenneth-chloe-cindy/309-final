from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE
from studios.models import Studio

# based on https://stackoverflow.com/questions/5966629/django-days-of-week-representation-in-model
DAYS_OF_WEEK = (
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
)


class ClassOffering(models.Model):
    name = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=200, null=False)
    coach = models.CharField(max_length=200, null=False)
    times = models.CharField(max_length=200, null=False)
    capacity = models.PositiveIntegerField(null=False)
    end_recursion_date = models.DateField()
    studio = models.ForeignKey(to=Studio, on_delete=CASCADE)


class TimeInterval(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    day = models.IntegerField(choices=DAYS_OF_WEEK)
    class_offering = models.ForeignKey(to=ClassOffering, on_delete=CASCADE)


class Keyword(models.Model):
    keyword = models.CharField(max_length=200, null=False)
    class_offering = models.ForeignKey(to=ClassOffering, on_delete=CASCADE)


class ClassInstance(models.Model):
    date = models.DateField()
    capacity_count = models.PositiveIntegerField(default=0, null=False)
    class_offering = models.ForeignKey(to=ClassOffering, on_delete=CASCADE,
                                       related_name='class_offering')


class UserEnroll(models.Model):
    class_instance = models.ForeignKey(to=ClassInstance, on_delete=CASCADE)
    class_offering = models.ForeignKey(to=ClassOffering, on_delete=CASCADE)
    # TODO: Actually add a user
