from django.urls import path, include, re_path
# from studios.views import StudioListView, CreateStudioView, EditStudioView, DeleteStudioView, RetrieveStudioView
from .views import StudioListView, RetrieveStudioView, RetrieveAmenitiesView, RetrieveStudioImageView, StudioMapsDirectionsView, StudioListFilterView, StudioListFilterClassesView, StudioClassListView
# CreateStudioView, EditStudioView, DeleteStudioView, CreateAmenityView

app_name = 'studios'

# The admin site studio views are commented out because they should only be accessible via the Admin Site.
urlpatterns = [
    path('list/', StudioListView.as_view()),
    path('list/filter/', StudioListFilterView.as_view()),
    path('<studio_id>/classes/list/', StudioClassListView.as_view()),
    path('<studio_id>/', RetrieveStudioView.as_view()),
    path('<studio_id>/amenities/list/', RetrieveAmenitiesView.as_view()),
    path('<studio_id>/images/list/', RetrieveStudioImageView.as_view()),
    path('<studio_id>/classes/filter/', StudioListFilterClassesView.as_view()),
    path('<studio_id>/directions/', StudioMapsDirectionsView.as_view()),

    # Below are depreciated URLs
    # path('new/', CreateStudioView.as_view()),
    # path('<studio_id>/edit/', EditStudioView.as_view()),
    # path('<studio_id>/delete/', DeleteStudioView.as_view()),
    # path('amenity/new/', CreateAmenityView.as_view()),
    # path('amenity/<amenity_id>/edit/', EditStudioView.as_view()),
]
