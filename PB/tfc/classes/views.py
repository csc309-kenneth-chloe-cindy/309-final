from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import ClassInstance, ClassOffering
from rest_framework.response import Response
from .exceptions import AlreadyEnrolledException, FullCapacityException, NotSubscribedException, \
    TargetInPastException

from .serializers import ClassOfferingSerializer, ClassInstanceSerializer


# Create your views here.
class EnrollFuture(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        class_offering = get_object_or_404(ClassOffering, pk=kwargs['class_id'])
        enrolled_classes = None
        try:
            enrolled_classes = class_offering.enroll_user(user)
        except (NotSubscribedException):
            return Response({"Message": "User is not subscribed"},
                            status=status.HTTP_400_BAD_REQUEST)
        except (TargetInPastException):
            return Response({"Message": "Enrollment target is in the past"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"Message": f"Enrolled in {len(enrolled_classes)} classes"},
                        status=status.HTTP_200_OK)


class EnrollSingleInstance(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        class_instance = get_object_or_404(ClassInstance, pk=kwargs['class_id'])
        ret = None
        try:
            ret = class_instance.enroll_user(user)
        except (TargetInPastException):
            return Response({"Message": "Enrollment target is in the past"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except (NotSubscribedException):
            return Response({"Message": "User is not subscribed"},
                            status=status.HTTP_400_BAD_REQUEST)
        except (FullCapacityException):
            return Response({"Message": "Class at full capacity"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except (AlreadyEnrolledException):
            return Response({"Message": "User already enrolled"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = ClassInstanceSerializer(ret)
        return Response(serializer.data, status=status.HTTP_200_OK)
