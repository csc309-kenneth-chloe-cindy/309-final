from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TFCUserSerializer
from .models import TFCUser
from classes.models import ClassOffering, UserEnroll
from classes.serializers import ClassOfferingSerializer


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


class RetrieveClassScheduleView(APIView):
    serializer_class = ClassOfferingSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        filtered_lst = UserEnroll.objects.filter(user__id=user_id).order_by('class_offering')

        schedule = list(set([o.class_offering for o in filtered_lst]))

        print(schedule)

        serialized_lst = [ClassOfferingSerializer(c).data for c in schedule]

        page_class_lst = Paginator(serialized_lst, 10)

        pg = request.GET.get("page")

        if pg is not None:
            page_num = int(pg)

            # If you have only 2 pages, but the query param sends in page=3,
            # it will just return the last page (page 2)
            return Response(page_class_lst.get_page(page_num).object_list)
        else:
            # Defaults to returning the whole list of studios if no page is given.
            return Response(serialized_lst)


class RetrieveClassHistoryView(APIView):
    # serializer_class = ClassOfferingSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        return Response(user_id)