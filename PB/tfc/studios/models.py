from django.db import models
from django.db.models import CASCADE

# Create your models here.
#
# class Studio(models.Model):
#     name = models.CharField(max_length=200, null=False)
#     address = models.CharField(max_length=200, null=False)
#     postal_code = models.CharField(max_length=200, null=False)
#     phone_num = models.CharField(max_length=200, null=False)
#     longitude = models.CharField(max_length=200, null=False)
#     latitude = models.CharField(max_length=200, null=False)
#
#     def __str__(self):
#         return self.name
#
# class StudioImage(models.Model):
#     studio = models.ForeignKey(to=Studio, on_delete=CASCADE, related_name='studio_image')
#     image = models.ImageField()
#
#     def __str__(self):
#         return self.name
#
# class StudioAmenities(models.Model):
#     name = models.CharField(max_length=200, null=False)
#     quantity = models.PositiveIntegerField(max_length=200, null=False)
#     studio = models.ForeignKey(to=Studio, on_delete=CASCADE, related_name='amenities')
#
#     def __str__(self):
#         return self.name
