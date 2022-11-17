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
from classes.serializers import ClassOfferingSerializer, ClassInstanceSerializer
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
    """
    Retrieves a studio with the id `studio_id`.
    """
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
    """
    Retrieves a list of studios that are sorted to closest -> furthest from the lat/long passed in
    from the frontend.

    Sample payload:
        ```{
        "latitude": "43.65792466303926",
        "longitude": "-79.39900559414212"
        }```

    Params:
        `?page=` - Specifies the page # of the list of studios.
    """
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination

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


class StudioListFilterView(APIView):
    """
    Returns a list of studios, filtered by the filter choices below:

    Filter choices are:
        `name` of the Studio, `amenities`, `class_offering_name`, `coach_name`

    Sample payload:
        `{
            "amenities": ["Pool", "Gym"],
            "name": "Pythonic Fitness Studio",
            "class_offering_name": "Pilates",
            "coach_name": "Mr. B"
        }`
    """
    serializer_class = StudioSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        raw_filters = request.data

        filters = {}

        amen_lst = []

        for k in raw_filters:
            if k == "name":
                filters["name"] = raw_filters[k]

            if k == "class_offering_name":
                filters["classoffering__name"] = raw_filters[k]

            if k == "coach_name":
                filters["classoffering__coach"] = raw_filters[k]

            if k == "amenities":
                amen_lst = raw_filters[k]

        filtered_lst = Studio.objects.filter(**filters)

        if amen_lst:
            for x in amen_lst:
                filtered_lst = filtered_lst.filter(Q(amenities__name=x)).distinct()
                # Keep on filtering based on the amenities

        serialized_lst = [StudioSerializer(i).data for i in filtered_lst]

        page_studio_lst = Paginator(serialized_lst, 10)

        pg = request.GET.get("page")

        if pg is not None:
            page_num = int(pg)

            # If you have only 2 pages, but the query param sends in page=3,
            # it will just return the last page (page 2)
            return Response(page_studio_lst.get_page(page_num).object_list)
        else:
            # Defaults to returning the whole list of studios if no page is given.
            return Response(serialized_lst)


class StudioListFilterClassesView(APIView):
    """
    Returns a list of classes offered by Studio with `studio_id`, filtered by the filter choices below:

    Filter choices are:
        `class_name`, `coach_name`, `date`, `start_time`, `end_time`

    Sample payload:
        ```{
            "date": "2",
            "class_name": "Pilates",
            "coach_name": "Mr. B",
            "start_time": "6:00",
            "end_time": "7:00"
        }```
    """
    serializer_class = ClassOfferingSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, studio_id):
        raw_filters = request.data

        filters = {"studio": studio_id}

        for k in raw_filters:
            if k == "class_name":
                filters["name"] = raw_filters[k]

            if k == "coach_name":
                filters["coach"] = raw_filters[k]

            if k == "date":
                filters["timeinterval__day"] = raw_filters[k]

            if k == "start_time":
                formatted_time = datetime.strptime(raw_filters[k], '%H:%M').time()

                filters["timeinterval__start_time"] = formatted_time

            if k == "end_time":
                formatted_time = datetime.strptime(raw_filters[k], '%H:%M').time()

                filters["timeinterval__end_time"] = formatted_time

        filtered_lst = ClassOffering.objects.filter(**filters)

        serialized_lst = [ClassOfferingSerializer(i).data for i in filtered_lst]

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


class StudioMapsDirectionsView(APIView):
    """
    Returns a Google Maps link that has the destination set to the studio specified by `studio_id`.

    Example Output: `https://www.google.com/maps/dir/?api=1&destination=43.661430,-79.397000`
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, studio_id):
        link_base = "https://www.google.com/maps/dir/?api=1&destination="

        studio = get_object_or_404(Studio, id=studio_id)  # Studio.objects.get(id=studio_id)

        studio_lat = studio.latitude
        studio_long = studio.longitude

        link_base = link_base + str(studio_lat) + "," + str(studio_long)

        return Response(link_base)


class StudioClassListView(APIView, LimitOffsetPagination):
    """
    Returns a list of all ClassOfferings held by studio with `studio_id`, and sends a paginated
    list of ClassInstances associated with the ClassOfferings, sorted in ascending order by the
    date of the ClassInstance.

    Params:
        `?page=` - Specifies the page # of the list of classes.
    """

    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination

    def get(self, request, studio_id):
        class_offerings = get_list_or_404(ClassOffering, studio_id=studio_id)
        pg = request.GET.get("page")
        offerings_to_instances = []

        for c in class_offerings:
            today = datetime.now()
            # print("THIS IS THE DATE RIGHT NOW: {0}".format(today))

            instances = ClassInstance.objects.filter(Q(class_offering=c.id) & Q(date__gte=today))

            filtered_lst = []

            for i in instances:
                combined_date = datetime.combine(i.date, i.time_interval.start_time)

                if combined_date > today:
                    serialized_inst = ClassInstanceSerializer(i)
                    filtered_lst.append((serialized_inst.data, combined_date))

            filtered_lst.sort(key=lambda tup: tup[1])

            sorted_lst = []

            for t in filtered_lst:
                sorted_lst.append(t[0])

            serialized_class = ClassOfferingSerializer(c)
            pag_sorted_lst = Paginator(sorted_lst, 5)

            offerings_to_instances.append((serialized_class.data, pag_sorted_lst))

        class_lst = []

        for o in offerings_to_instances:
            curr = {"class_details": o[0]}

            if pg is not None:
                page_num = int(pg)

                pag_class_lst = o[1].get_page(page_num).object_list

                curr["class_instances"] = pag_class_lst
            else:
                curr["class_instances"] = o[1]

            class_lst.append(curr)

        return Response(class_lst)


"""
    STUDIO IMAGES

    Below are views that deal with creating, retrieving and editing images associated with a studio. 
"""


class CreateStudioImageView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = StudioImageSerializer


class RetrieveStudioImageView(ListAPIView, LimitOffsetPagination):
    """
    Returns a list of all images under the Studio with `studio_id`

    Params:
        `?page=` - Specifies the page # of the list of studio images.
    """
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
    """
    Returns a list of all amenities offered by studio with `studio_id`.

    Params:
        `?page=` - Specifies the page # of the list of amenities.
    """
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
