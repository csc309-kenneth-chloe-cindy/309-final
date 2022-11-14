from django.urls import path
from .views import (
    SubscriptionDetail,
    UpdatePaymentMethodView
)

app_name = 'subscriptions'

urlpatterns = [
    path('subscription/', SubscriptionDetail.as_view()),
    path('payment_method/<int:pk>/', UpdatePaymentMethodView.as_view())
]
