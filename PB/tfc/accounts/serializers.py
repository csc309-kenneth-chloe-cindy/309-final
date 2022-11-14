from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models import TFCUser


class TFCUserSerializer(serializers.ModelSerializer):
    # username = serializers.ReadOnlyField()

    class Meta:
        model = TFCUser
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'phone_number', 'avatar']

    def create(self, validated_data):
        user = TFCUser(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            avatar=validated_data['avatar'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
