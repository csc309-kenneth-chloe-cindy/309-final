from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .models import ClassOffering, TimeInterval, Keyword, ClassInstance, UserEnroll
from studios.serializers import StudioSerializer
import datetime

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
    
    def create(self, validated_data):
        class_offering_data = validated_data.pop("class_offering")
        class_offering = ClassOffering.objects.create(**class_offering_data)
        weekday = TimeInterval.objects.filter(class_offering=class_offering).day
        date = datetime.date.today()
        end_date = class_offering.end_recursion_date
        if weekday - date.weekday() <= 0:
            date = datetime.timedelta(weekday - date.weekday() + 7)
        else:
            date = datetime.timedelta(weekday - date.weekday())
        list = []
        while date <= end_date:
            list = list.append(ClassInstance(date=date, capacity_count=0, class_offering=class_offering))
            date = datetime.timedelta(7)
        class_instance = ClassInstance.objects.bulk_create(list)
        return class_instance      

    class Meta:
        model = ClassInstance
        fields = ['date', 'capacity_count', 'class_offering']

class UserEnrollSerializer(serializers.ModelSerializer):
    class_offering = ClassOfferingSerializer()
    class_instance = ClassInstanceSerializer()

    class Meta:
        model = UserEnroll
        fields = ['class_instance', 'class_offering']
