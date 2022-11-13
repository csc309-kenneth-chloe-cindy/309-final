from rest_framework import serializers

from .models import TFCUser


class TFCUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TFCUser
        fields = ['username', 'email', 'firstname', 'lastname', 'phone_number', 'avatar']
