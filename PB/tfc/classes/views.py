from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from classes.models import ClassOffering, ClassInstance
from django.views.generic import TemplateView, ListView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from classes.serializers import ClassOfferingSerializer, TimeIntervalSerializer, KeywordSerializer, ClassInstanceSerializer, UserEnrollSerializer
from studios.models import Studio
import pandas as pd
import datetime
from datetime import date, timedelta
from .models import TimeInterval, Keyword

# Create your views here.
"""
    CLASS_OFFERING
"""
class CreateClassOfferingView(CreateAPIView):
    #permission_classes = [IsAdminUser]
    serializer_class = ClassOfferingSerializer

class EditClassOfferingView(RetrieveAPIView, UpdateAPIView):
    serializer_class = ClassOfferingSerializer
    #permission_classes = [IsAdminUser]

    def get_object(self):
        return get_object_or_404(ClassOffering, id=self.kwargs['class_offering_id'])

class DeleteClassOfferingView(DestroyAPIView):
    serializer_class = ClassOfferingSerializer
    #permission_classes = [IsAdminUser]


"""
    TIME_INTERVAL
"""

class CreateTimeIntervalView(CreateAPIView):
    #permission_classes = [IsAdminUser]
    serializer_class = TimeIntervalSerializer

class EditTimeIntervalView(RetrieveAPIView, UpdateAPIView):
    serializer_class = TimeIntervalSerializer
    #permission_classes = [IsAdminUser]

    def get_query(self):
        return TimeInterval.objects.filter(class_offering=self.kwargs['class_offering_id'])

"""
    KEY_WORD
"""

class CreateKeywordView(CreateAPIView):
    #permission_classes = [IsAdminUser]
    serializer_class = KeywordSerializer

class EditKeywordView(RetrieveAPIView, UpdateAPIView):
    serializer_class = KeywordSerializer
    #permission_classes = [IsAdminUser]

    def get_query(self):
        return Keyword.objects.filter(studio=self.kwargs['studio_id'])

"""
    CLASS_INSTANCE
"""

class CreateClassInstanceView(CreateAPIView):
    #permission_classes = [IsAdminUser]
    serializer_class = ClassInstanceSerializer

class DeleteAllClassInstanceView(DestroyAPIView):
    #permission_classes = [IsAdminUser]
    serializer_class = ClassInstanceSerializer

    def get_query(self):
        list = ClassInstance.filter(class_offering=self.kwargs['class_offering_id'])
        new_list = []
        for class_instance in list:
            if class_instance.date > datetime.date.today():
                new_list = new_list + class_instance
        return new_list

class DeleteSingleClassInstanceView(DestroyAPIView):
    #permission_classes = [IsAdminUser]
    serializer_class = ClassInstanceSerializer
    def get_object(self):
        return get_object_or_404(ClassInstance, id=self.kwargs['class_instance_id'])
