from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import ClassInstance, ClassOffering
from rest_framework.response import Response
from .exceptions import EnrollmentException, CapacityException, NotSubscribedException, \
    TargetInPastException

from .serializers import ClassOfferingSerializer, ClassInstanceSerializer


class UnenrollFuture(APIView):
    """
    Unenrolls a user from all future instances of a class, pointed to by <class_id>.
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        """
        delete:
        Unenrolls the user from all future instances of a particular class, specified by `class_id`.
        """
        user = request.user
        class_offering = get_object_or_404(ClassOffering, pk=kwargs['class_id'])
        num_deleted = 0
        try:
            num_deleted = class_offering.unenroll_user(user)
        except (NotSubscribedException):
            return Response({"Message": "User is not subscribed"},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({"Message": f"Unenrolled in {num_deleted} classes"},
                        status=status.HTTP_200_OK)


class UnenrollSingle(APIView):
    """
    Unenrolls a user from one instance of a class, pointed to by <class_id>.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        """
        delete:
        Unenrolls the user from one instance of a particular class, specified by `class_id`.
        """
        user = request.user
        class_instance = get_object_or_404(ClassInstance, pk=kwargs['class_id'])
        try:
            class_instance.unenroll_user(user)
        except (TargetInPastException):
            return Response({"Message": "Unenrollment target is in the past"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except (NotSubscribedException):
            return Response({"Message": "User is not subscribed"},
                            status=status.HTTP_400_BAD_REQUEST)
        except (CapacityException):
            return Response({"Message": "Class is already empty"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except (EnrollmentException):
            return Response({"Message": "User already unenrolled"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_204_NO_CONTENT)


# Create your views here.
class EnrollFuture(APIView):
    """
    Enrolls a user to all future instances of a class, pointed to by <class_id>.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        post:
        Enrolls a user to all future instances of a class, pointed to by <class_id>.
        """
        user = request.user
        class_offering = get_object_or_404(ClassOffering, pk=kwargs['class_id'])
        enrolled_classes = None
        try:
            enrolled_classes = class_offering.enroll_user(user)
        except (NotSubscribedException):
            return Response({"Message": "User is not subscribed"},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({"Message": f"Enrolled in {len(enrolled_classes)} classes"},
                        status=status.HTTP_200_OK)


class EnrollSingleInstance(APIView):
    """
    Enrolls a user to one instances of a class, pointed to by <class_id>.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        post:
        Enrolls a user to one instances of a class, pointed to by <class_id>.
        """
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
        except (CapacityException):
            return Response({"Message": "Class at full capacity"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except (EnrollmentException):
            return Response({"Message": "User already enrolled"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = ClassInstanceSerializer(ret)
        return Response(serializer.data, status=status.HTTP_200_OK)
