from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from studios.models import Studio, StudioImage, StudioAmenities
from django.shortcuts import get_object_or_404
from studios.serializers import StudioSerializer, AmenitySerializer, StudioImageSerializer
from geopy import distance
from rest_framework.response import Response

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


class StudioListView(APIView):
    permission_classes = [IsAuthenticated]

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

        # print(studios)

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

        studio = Studio.objects.get(id=studio_id)

        studio_lat = studio.latitude
        studio_long = studio.longitude

        link_base = link_base + str(studio_lat) + "," + str(studio_long)

        # print(link_base)

        return Response(link_base)


"""
    STUDIO IMAGES

    Below are views that deal with creating, retrieving and editing images associated with a studio. 
"""


class CreateStudioImageView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = StudioImageSerializer


class RetrieveStudioImageView(ListAPIView):
    serializer_class = StudioImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StudioImage.objects.filter(studio=self.kwargs['studio_id'])


"""
    AMENITIES
    
    Below are views that deal with creating, retrieving and editing amenities. 
"""


class CreateAmenityView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AmenitySerializer


class RetrieveAmenitiesView(ListAPIView):
    serializer_class = AmenitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StudioAmenities.objects.filter(studio=self.kwargs['studio_id'])


class EditAmenityView(UpdateAPIView):
    serializer_class = AmenitySerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        return get_object_or_404(Studio, id=self.kwargs['amenity_id'])
