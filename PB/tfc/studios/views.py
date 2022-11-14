from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from studios.models import Studio, StudioImage, StudioAmenities
from django.shortcuts import get_object_or_404
from studios.serializers import StudioSerializer, AmenitySerializer, StudioImageSerializer
from geopy import distance
from rest_framework.response import Response


# Create your views here.
class StudioListView(APIView):
    permission_classes = [IsAuthenticated]

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


class CreateStudioImageView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = StudioImageSerializer


class CreateAmenityView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AmenitySerializer


class EditAmenityView(RetrieveAPIView, UpdateAPIView):
    serializer_class = AmenitySerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        return get_object_or_404(Studio, id=self.kwargs['amenity_id'])
