from rest_framework import serializers

from .models import TFCUser


class TFCUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TFCUser
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'phone_number', 'avatar']
