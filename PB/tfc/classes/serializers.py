from rest_framework import serializers
from classes.models import ClassOffering, TimeInterval, ClassInstance
from studios.serializers import StudioSerializer
from classes.models import ClassOffering


class ClassOfferingSerializer(serializers.ModelSerializer):
    studio = StudioSerializer(read_only=True)
    studio_id = serializers.IntegerField(write_only=True)

    class Meta:
        fields = ["name", "description", "coach", "capacity", "end_recursion_date", "studio",
                  "studio_id"]
        model = ClassOffering

class TimeIntervalSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ["start_time", "end_time", "day"]
        model = TimeInterval


class ClassInstanceSerializer(serializers.ModelSerializer):
    # class_offering = ClassOfferingSerializer(read_only=True)
    time_interval = TimeIntervalSerializer(read_only=True)
    class Meta:
        fields = ["date", "capacity_count", "time_interval"]
        model = ClassInstance
