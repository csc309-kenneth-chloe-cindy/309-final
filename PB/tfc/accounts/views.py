from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.views import APIView


# Create your views here.
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        pass

