from django.urls import path
from .views import EnrollSingleInstance

app_name = 'classes'

urlpatterns = [
    path('class_instance_enroll/<int:class_id>/', EnrollSingleInstance.as_view())

]
