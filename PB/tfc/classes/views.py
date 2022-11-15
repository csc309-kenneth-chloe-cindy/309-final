from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from classes.models import ClassOffering, ClassInstance
from django.views.generic import TemplateView, ListView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from classes.serializers import ClassOfferingSerializer, TimeIntervalSerializer, KeywordSerializer, ClassInstanceSerializer, UserEnrollSerializer
from studios.models import Studio

# Create your views here.
class CreateClassView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ClassOfferingSerializer

class CancelAllClassView(RetrieveAPIView, DestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ClassOfferingSerializer

    def get_object(self):
        return get_object_or_404(ClassOffering, name=self.kwargs['class_name'], studio=self.kwargs['studio_name'])

class CancelClassInstanceView(RetrieveAPIView, DestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ClassInstanceSerializer

    def get_object(self):
        return get_object_or_404(ClassInstance, id=self.kwargs['class_instance_id'], studio=self.kwargs['studio_name'])

class EditClassView(RetrieveAPIView, UpdateAPIView):
    serializer_class = ClassOfferingSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        return get_object_or_404(ClassOffering, name=self.kwargs['class_name'], studio=self.kwargs['studio_name'])