from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import ClassInstance
from rest_framework.response import Response
from .exceptions import AlreadyEnrolledException, FullCapacityException


# Create your views here.

class EnrollSingleInstance(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # TODO: check for active subscription
        user = request.user
        print(user)
        class_instance = get_object_or_404(ClassInstance, pk=kwargs['class_id'])
        print(class_instance)
        try:
            class_instance.enroll_user(user)
        except (FullCapacityException):
            return Response({"Message": "Class at full capacity"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except (AlreadyEnrolledException):
            return Response({"Message": "User already enrolled"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_204_NO_CONTENT)
