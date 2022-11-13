from django.urls import path, include
from studios.views import StudioListView, CreateStudioView, EditStudioView, DeleteStudioView

app_name = 'studios'

urlpatterns = [
    path('list/', StudioListView.as_view()),
    path('new_studio/', CreateStudioView.as_view()),
    path('<str:studio_name>/edit_studio', EditStudioView.as_view()),
    path('<str:studio_name>/delete_studio', DeleteStudioView.as_view()),
    path('<str:amenity_name>/edit_amenities', EditStudioView.as_view()),
]
