from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import CreateUserView, UpdateUserProfileView

app_name = 'accounts'

urlpatterns = [
    # path('hello/', HelloView.as_view()),
    path('register/', CreateUserView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('<user_id>/update/', UpdateUserProfileView.as_view()),
]

# ABOUT:  path('login/', ...)
# The login flow uses the JWT built-in view to return an access token and a refresh token associated
# with the user that is logging in. The frontned should send the username and password to the backend as
# the payload.
# the Frontend should pull the "access" token from the 'return' of its call to the API
# and save that access token in memory until it expires.