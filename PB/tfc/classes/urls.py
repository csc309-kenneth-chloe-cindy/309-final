from django.urls import path
from .views import CreateClassView, CancelAllClassView, CancelClassInstanceView, EditClassView

app_name = 'classes'

urlpatterns = [
    path('<int:studio_id>/new/', CreateClassView.as_view()),
    path('<int:studio_id>/cancel/<int:class_id>/all/', CancelAllClassView.as_view()),
    path('<int:studio_id>/edit/<int:class_id>/', EditClassView.as_view()),
    path('<int:studio_id>/cancel/<int:class_id>/<int:class_instance_id>/', CancelClassInstanceView.as_view())
]
