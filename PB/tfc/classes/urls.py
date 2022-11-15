from django.urls import path
from .views import CreateClassView, CancelAllClassView, CancelClassInstanceView, EditClassView

app_name = 'classes'

urlpatterns = [
    path('<str:studio_name>/new_class/', CreateClassView.as_view()),
    path('<str:studio_name>/cancel/<str:class_name>/all_classes', CancelAllClassView.as_view()),
    path('<str:studio_name>/edit/<str:class_name>', EditClassView.as_view()),
    path('<str:studio_name>/cancel/<str:class_name>/<int:class_instance_id>', CancelClassInstanceView.as_view())
]
