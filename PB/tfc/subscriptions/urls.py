from django.urls import path
from .views import (
    SubscriptionDetail
)

app_name = 'subscriptions'

urlpatterns = [
    path('subscription', SubscriptionDetail.as_view())
]
