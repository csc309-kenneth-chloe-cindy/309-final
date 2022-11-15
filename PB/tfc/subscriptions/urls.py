from django.urls import path
from .views import (
    SubscriptionDetail,
    UpdatePaymentMethodView,
    GetPaymentHistory,
    DeleteSubscription
)

app_name = 'subscriptions'

urlpatterns = [
    path('subscription/', SubscriptionDetail.as_view()),
    path('subscription/<int:pk>/', DeleteSubscription.as_view()),
    path('payment_method/<int:pk>/', UpdatePaymentMethodView.as_view()),
    path('payment_history/<int:pk>/', GetPaymentHistory.as_view())
]
