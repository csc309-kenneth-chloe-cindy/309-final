from rest_framework import serializers
from studios.serializers import StudioSerializer
from classes.models import ClassOffering


class ClassOfferingSerializer(serializers.ModelSerializer):
    studio = StudioSerializer(read_only=True)
    studio_id = serializers.IntegerField(write_only=True)

    class Meta:
        fields = ["name", "description", "coach", "capacity", "end_recursion_date", "studio",
                  "studio_id"]
        model = ClassOffering
