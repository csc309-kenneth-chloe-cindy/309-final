from rest_framework import serializers
from .models import Studio, StudioImage, StudioAmenities


class StudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = ['name', 'address', 'postal_code', 'phone_num', 'longitude', 'latitude']


class StudioImageSerializer(serializers.ModelSerializer):
    # studio = StudioSerializer(read_only=True)

    class Meta:
        model = StudioImage
        fields = ['image']


class AmenitySerializer(serializers.ModelSerializer):
    studio = StudioSerializer(read_only=True)

    class Meta:
        model = StudioAmenities
        fields = ['name', 'quantity', 'studio']
