from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from studios.models import Studio, StudioImage, StudioAmenities
from django.views.generic import TemplateView, ListView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from studios.serializers import StudioSerializer, AmenitySerializer

# Create your views here.
class StudioListView(ListAPIView):
    serializer_class = StudioSerializer

    def get_queryset(self):
        return Studio.objects.all()

class CreateStudioView(RetrieveAPIView, CreateAPIView):
    #permission_classes = [IsAdminUser]
    serializer_class = StudioSerializer
    
class EditStudioView(RetrieveAPIView, UpdateAPIView):
    serializer_class = StudioSerializer
    #permission_classes = [IsAdminUser]

    def get_object(self):
        return get_object_or_404(Studio, name=self.kwargs['studio_name'])

class DeleteStudioView(RetrieveAPIView, DestroyAPIView):
    serializer_class = StudioSerializer
    #permission_classes = [IsAdminUser]

    def get_object(self):
        return get_object_or_404(Studio, name=self.kwargs['studio_name'])
    
class EditAmenityView(RetrieveAPIView, UpdateAPIView):
    serializer_class = AmenitySerializer
    #permission_classes = [IsAdminUser]

    def get_object(self):
        return get_object_or_404(Studio, name=self.kwargs['amenity_name'])
