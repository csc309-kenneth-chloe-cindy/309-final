from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from .serializers import TFCUserSerializer


# Create your views here.

class CreateUserView(CreateAPIView):
    serializer_class = TFCUserSerializer



class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        pass

