from django.urls import path, include
from rest_framework import routers
from studios import views

app_name = 'studios'

router = routers.DefaultRouter()
router.register(r'add/class', views.StudioViewList)

urlpatterns = [
    path('', include(router.urls)),
    
]
