from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .models import StudioModel

class StudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudioModel
        fields = "_all_"
