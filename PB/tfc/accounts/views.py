from django.shortcuts import render, get_object_or_404
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TFCUserSerializer
from .models import TFCUser


# Create your views here.

# This takes a POST request.
class CreateUserView(CreateAPIView):
    serializer_class = TFCUserSerializer


# Use PUT when you are updating *all* fields of the user profile.
# Use PATCH when updating *one* field of the user profile.
class UpdateUserProfileView(UpdateAPIView):
    serializer_class = TFCUserSerializer

    def get_object(self):
        return get_object_or_404(TFCUser, id=self.kwargs['user_id'])

# Uncomment this to test out how authentication
# class HelloView(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def get(self, request):
#         content = {'message': 'Hello, World!'}
#         return Response(content)