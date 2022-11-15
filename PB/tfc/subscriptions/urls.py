from django.urls import path
from .views import (
    SubscriptionDetail,
    UpdatePaymentMethodView,
    GetPaymentHistory,
    DeleteUpdateSubscription,
    UpdateSubscription
)

app_name = 'subscriptions'

urlpatterns = [
    path('subscription/', SubscriptionDetail.as_view()),
    path('subscription/<int:pk>/', DeleteUpdateSubscription.as_view()),
    path('subscription/update/<int:pk>/', UpdateSubscription.as_view()),
    path('payment_method/<int:pk>/', UpdatePaymentMethodView.as_view()),
    path('payment_history/<int:user_id>/', GetPaymentHistory.as_view())
]
