from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import CreateUserView

app_name = 'accounts'

urlpatterns = [
    path('register/', CreateUserView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
