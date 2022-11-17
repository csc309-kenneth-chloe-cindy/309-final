from django.urls import path
from .views import EnrollSingleInstance, EnrollFuture, UnenrollSingle, UnenrollFuture

app_name = 'classes'

urlpatterns = [
    path('enroll/single_class/<int:class_id>/', EnrollSingleInstance.as_view()),
    path('enroll/future_classes/<int:class_id>/', EnrollFuture.as_view()),
    path('unenroll/single_class/<int:class_id>/', UnenrollSingle.as_view()),
    path('unenroll/future_classes/<int:class_id>/', UnenrollFuture.as_view())

]
