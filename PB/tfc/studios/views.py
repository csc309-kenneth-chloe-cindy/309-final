from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from studios.serializers import StudioSerializer

@api_view(['GET', 'POST', 'DELETE'])
# Create your views here.
class studio_list(request):
    if request.method == 'GET':
        serializer = StudioSerializer()
