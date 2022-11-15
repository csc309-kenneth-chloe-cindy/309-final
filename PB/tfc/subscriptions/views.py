from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from .models import Subscription, SubscriptionPlan, PaymentMethod, PaymentHistory, get_period
from django.shortcuts import get_object_or_404
from .serializers import SubscriptionSerializer, PaymentHistorySerializer, PaymentMethodSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer


# Create your views here.


class UpdatePaymentMethodView(UpdateAPIView):
    serializer_class = PaymentMethodSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(PaymentMethod, pk=self.kwargs['pk'])


class GetPaymentHistory(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # payment history object -> search for subscription plan with this id
        print(kwargs)
        payment_history = get_object_or_404(PaymentHistory, pk=kwargs["pk"])
        print("found payment history")

        subscription_plan = get_object_or_404(Subscription,
                                              payment_method=payment_history.payment_method)
        future_payment = subscription_plan.subscription_type.price

        print(future_payment)

        payment_history_serializer = PaymentHistorySerializer(payment_history)
        response_data = payment_history_serializer.data
        response_data["future_payment"] = {"price": future_payment,
                                           "date": subscription_plan.next_payment_date}

        return Response(response_data, status=status.HTTP_200_OK)


class SubscriptionDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Subscription, pk=pk)

    def delete(self, request, *args, **kwargs):
        subscription = self.get_object(kwargs['pk'])

        # drop classes

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
