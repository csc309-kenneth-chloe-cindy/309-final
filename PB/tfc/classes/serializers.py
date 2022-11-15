from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .models import ClassOffering, TimeInterval, Keyword, ClassInstance, UserEnroll
from studios.serializers import StudioSerializer

class ClassOfferingSerializer(serializers.ModelSerializer):
    studio = StudioSerializer()
    class Meta:
        model = ClassOffering
        fields = ['name', 'description', 'coach', 'times', 'capacity', 'end_recursion_date', 'studio']

class TimeIntervalSerializer(serializers.ModelSerializer):
    class_offering = ClassOfferingSerializer()

    class Meta:
        model = TimeInterval
        fields = ['start_time', 'end_time', 'day', 'class_offering']

class KeywordSerializer(serializers.ModelSerializer):
    class_offering = ClassOfferingSerializer()

    class Meta:
        model = Keyword
        fields = ['keyword', 'class_offering']

class ClassInstanceSerializer(serializers.ModelSerializer):
    class_offering = ClassOfferingSerializer()

    class Meta:
        model = ClassInstance
        fields = ['date', 'capacity_count', 'class_offering']

class UserEnrollSerializer(serializers.ModelSerializer):
    class_offering = ClassOfferingSerializer()
    class_instance = ClassInstanceSerializer()

    class Meta:
        model = UserEnroll
        fields = ['class_instance', 'class_offering']
