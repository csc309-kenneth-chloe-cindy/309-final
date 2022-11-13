from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .models import Studio, StudioImage, StudioAmenities

class StudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = ['name', 'address', 'postal_code', 
        'phone_num', 'longitude', 'latitude']

class StudioImageSerializer(serializers.ModelSerializer):
    studio = StudioSerializer()

    class Meta:
        model = StudioImage
        fields = ['studio', 'image']

class AmenitySerializer(serializers.ModelSerializer):
    studio = StudioSerializer()

    class Meta:
        model = StudioAmenities
        fields = ['name', 'quantity', 'studio']
