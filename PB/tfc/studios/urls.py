from django.urls import path, include
# from studios.views import StudioListView, CreateStudioView, EditStudioView, DeleteStudioView, RetrieveStudioView
from .views import StudioListView, RetrieveStudioView, RetrieveAmenitiesView
# CreateStudioView, EditStudioView, DeleteStudioView, CreateAmenityView

app_name = 'studios'

# The admin site studio views are commented out because they should only be accessible via the Admin Site.
urlpatterns = [
    path('list/', StudioListView.as_view()),
    path('<studio_id>/', RetrieveStudioView.as_view()),
    path('<studio_id>/amenities/list/', RetrieveAmenitiesView.as_view()),
    # path('new/', CreateStudioView.as_view()),
    # path('<studio_id>/edit/', EditStudioView.as_view()),
    # path('<studio_id>/delete/', DeleteStudioView.as_view()),
    # path('amenity/new/', CreateAmenityView.as_view()),
    # path('amenity/<amenity_id>/edit/', EditStudioView.as_view()),
]
