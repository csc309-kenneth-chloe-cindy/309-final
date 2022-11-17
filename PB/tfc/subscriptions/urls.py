from django.urls import path
from .views import (
    SubscriptionDetail,
    UpdatePaymentMethodView,
    GetPaymentHistory,
)

app_name = 'subscriptions'

urlpatterns = [
    path('subscription/', SubscriptionDetail.as_view()),
    path('payment_method/', UpdatePaymentMethodView.as_view()),
    path('payment_history/', GetPaymentHistory.as_view())
]
