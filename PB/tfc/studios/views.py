from django.core.paginator import Paginator
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from studios.models import Studio, StudioImage, StudioAmenities
from django.shortcuts import get_object_or_404, get_list_or_404
from studios.serializers import StudioSerializer, AmenitySerializer, StudioImageSerializer
from geopy import distance
from rest_framework.response import Response
from classes.models import ClassOffering, ClassInstance, TimeInterval
from classes.serializers import ClassOfferingSerializer
from django.db.models import Q
from datetime import *

"""
    STUDIO

    Below are views that deal with creating, retrieving, editing/updating and deleting studio objects. 
"""


class CreateStudioView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = StudioSerializer


class RetrieveStudioView(RetrieveAPIView):
    serializer_class = StudioSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Studio, id=self.kwargs['studio_id'])


class EditStudioView(UpdateAPIView):
    serializer_class = StudioSerializer
    permission_classes = [IsAdminUser]


class DeleteStudioView(DestroyAPIView):
    serializer_class = StudioSerializer
    permission_classes = [IsAdminUser]


class StudioListView(APIView, LimitOffsetPagination):
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination

    """
    Gets a list of studios that are sorted to closest -> furthest from the lat/long passed in
    from the frontend.
    """

    def get(self, request):
        studio_list = Studio.objects.all()
        user_location = (request.data['latitude'], request.data['longitude'])

        studio_to_distance = []

        for studio in studio_list:
            studio_location = (studio.latitude, studio.longitude)

            dist = distance.distance(user_location, studio_location)

            serialized_studio = StudioSerializer(studio)

            studio_to_distance.append((serialized_studio.data, dist))

        studio_to_distance.sort(key=lambda tup: tup[1])

        studios = [i[0] for i in studio_to_distance]

        page_studio_lst = Paginator(studios, 15)
        # print(page_studio_lst.page(1).object_list)

        # print(studios)

        pg = request.GET.get("page")

        if pg is not None:
            page_num = int(pg)
            # print(page_num)

            # If you have only 2 pages, but the query param sends in page=3,
            # it will just return the last page (page 2)
            return Response(page_studio_lst.get_page(page_num).object_list)
        else:
            # Defaults to returning the whole list of studios if no page is given.
            return Response(studios)


class StudioMapsDirectionsView(APIView):
    permission_classes = [IsAuthenticated]

    """
    Returns a Google Maps link that has the destination set to the studio specified.
    
    Example: https://www.google.com/maps/dir/?api=1&origin=43.662625,-79.398640&destination=43.661430,-79.397000
    Example 2: https://www.google.com/maps/dir/?api=1&destination=43.661430,-79.397000
    """

    def get(self, request, studio_id):
        link_base = "https://www.google.com/maps/dir/?api=1&destination="

        studio = get_object_or_404(Studio, id=studio_id)  # Studio.objects.get(id=studio_id)

        studio_lat = studio.latitude
        studio_long = studio.longitude

        link_base = link_base + str(studio_lat) + "," + str(studio_long)

        # print(link_base)

        return Response(link_base)


class StudioClassListView(APIView, LimitOffsetPagination):
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination

    def get(self, request, studio_id):
        class_offerings = get_list_or_404(ClassOffering, studio_id=studio_id)

        offerings_to_instances = []

        for c in class_offerings:
            today = date.today()
            right_now = time(5, 0, 0) # datetime.now().time() TODO: remove this later

            cls = TimeInterval.objects.get(class_offering=c.id)
            print(cls.start_time)
            print(cls.start_time > right_now)

            instances = ClassInstance.objects.filter(Q(class_offering=c.id) & Q(date__gt=today))

            # instances_after_right_now = instances.filter(class_offering__gt)


            # ClassInstance.objects.filter(date__gt=today)
            # ClassInstance.objects.filter(Q(class_offering=c.id) & Q(date__gt=today))
            # ClassInstance.objects.filter(class_offering=c.id)

            # print(c)
            print(instances)

            offerings_to_instances.append((c))

        # print(class_offerings)

        return Response(1)


"""
    STUDIO IMAGES

    Below are views that deal with creating, retrieving and editing images associated with a studio. 
"""


class CreateStudioImageView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = StudioImageSerializer


class RetrieveStudioImageView(ListAPIView, LimitOffsetPagination):
    serializer_class = StudioImageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        studio_images = get_list_or_404(StudioImage, studio=self.kwargs['studio_id'])

        return studio_images  # StudioImage.objects.filter(studio=self.kwargs['studio_id'])


"""
    AMENITIES
    
    Below are views that deal with creating, retrieving and editing amenities. 
"""


class CreateAmenityView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AmenitySerializer


class RetrieveAmenitiesView(ListAPIView, LimitOffsetPagination):
    serializer_class = AmenitySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        studio_amenities = get_list_or_404(StudioAmenities, studio=self.kwargs['studio_id'])

        return studio_amenities


class EditAmenityView(UpdateAPIView):
    serializer_class = AmenitySerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        return get_object_or_404(Studio, id=self.kwargs['amenity_id'])
