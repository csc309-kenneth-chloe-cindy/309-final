from django.urls import path
from .views import CreateClassOfferingView, EditClassOfferingView, DeleteClassOfferingView, CreateTimeIntervalView, EditTimeIntervalView
from .views import CreateKeywordView, EditKeywordView, CreateClassInstanceView, DeleteAllClassInstanceView, DeleteSingleClassInstanceView

app_name = 'classes'

urlpatterns = [
    path('<studio_id>/new/', CreateClassOfferingView.as_view()),
    path('<studio_id>/edit/', EditClassOfferingView.as_view()),
    path('<studio_id>/delete/', DeleteClassOfferingView.as_view()),
    path('<class_offering_id>/new/time/', CreateTimeIntervalView.as_view()),
    path('<class_offering_id>/edit/time/', EditTimeIntervalView.as_view()),
    path('<class_offering_id>/new/keyword/', CreateKeywordView.as_view()),
    path('<class_offering_id>/edit/keyword/', EditKeywordView.as_view()),
    path('<class_offering_id>/add/instances/', CreateClassInstanceView.as_view()),
    path('<class_offering_id>/delete/all/', DeleteAllClassInstanceView.as_view()),
    path('<class_offering_id>/delete/<class_instance_id>/', DeleteSingleClassInstanceView.as_view())
]
