from django.urls import path, include
from studios.views import StudioListView, CreateStudioView, EditStudioView, DeleteStudioView
# from .views import StudioListView, CreateStudioView, EditStudioView, DeleteStudioView

app_name = 'studios'

urlpatterns = [
    path('list/', StudioListView.as_view()),
    path('new_studio/', CreateStudioView.as_view()),
    path('<studio_id>/edit/', EditStudioView.as_view()),
    path('<studio_id>/delete/', DeleteStudioView.as_view()),
    path('<amenity_id>/edit/', EditStudioView.as_view()),
]
