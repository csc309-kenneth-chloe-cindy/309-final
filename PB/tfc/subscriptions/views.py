from rest_framework import status
from rest_framework.views import APIView
from .models import Subscription, SubscriptionPlan
from django.shortcuts import get_object_or_404
from .serializers import SubscriptionSerializer, PaymentHistorySerializer
from rest_framework.response import Response


# Create your views here.
class SubscriptionDetail(APIView):

    def get_object(self, pk):
        return get_object_or_404(Subscription, pk=pk)

    def post(self, request, *args, **kwargs):
        subscription_serializer = SubscriptionSerializer(data=request.data,
                                                         context={'user': request.user})
        if subscription_serializer.is_valid():
            subscription = subscription_serializer.save()
            payment_method = subscription.payment_method

            payment_amount = get_object_or_404(SubscriptionPlan,
                                               pk=subscription.subscription_type.id).price

            payment_history_serializer = PaymentHistorySerializer(
                data={"amount": payment_amount, "payment_method_id": payment_method.id})
            if payment_history_serializer.is_valid():
                payment_history_serializer.save()
            else:
                return Response(payment_history_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

            return Response(subscription_serializer.data, status=status.HTTP_201_CREATED)

        return Response(subscription_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
