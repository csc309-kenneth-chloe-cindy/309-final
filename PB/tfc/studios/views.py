from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from studios.serializers import StudioSerializer
from studios.models import StudioModel

# Create your views here.
class StudioViewList(viewsets.ModelViewSet):
    queryset = StudioModel.objects.all()
    serializer_class = StudioSerializer
    
