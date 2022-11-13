from django.db import models
from django.db.models import CASCADE


# Create your models here.
#
class Studio(models.Model):
    name = models.CharField(max_length=200, null=False)
    address = models.CharField(max_length=200, null=False)
    postal_code = models.CharField(max_length=200, null=False)
    phone_num = models.CharField(max_length=200, null=False)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name


class StudioImage(models.Model):
    studio = models.ForeignKey(to=Studio, on_delete=CASCADE, related_name='studio_images')
    image_as_blob = models.BinaryField()


class StudioAmenities(models.Model):
    name = models.CharField(max_length=200, null=False)
    quantity = models.PositiveIntegerField(null=False)
    studio = models.ForeignKey(to=Studio, on_delete=CASCADE, related_name='amenities')

    def __str__(self):
        return self.name