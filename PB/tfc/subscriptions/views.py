from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from .models import Subscription, SubscriptionPlan, PaymentMethod, PaymentHistory, get_period
from classes.models import ClassInstance
from django.shortcuts import get_list_or_404, get_object_or_404
from .serializers import SubscriptionSerializer, PaymentHistorySerializer, PaymentMethodSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from dateutil.relativedelta import relativedelta


# Create your views here.


class UpdatePaymentMethodView(UpdateAPIView):
    serializer_class = PaymentMethodSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(PaymentMethod, pk=self.kwargs['pk'])


class GetPaymentHistory(APIView, LimitOffsetPagination):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        print(kwargs)
        user_id = kwargs["user_id"]
        subscription = get_object_or_404(Subscription, user=user_id)

        payment_historys = get_list_or_404(PaymentHistory,
                                           payment_method=subscription.payment_method.id)
        print("found payment history")
        print(payment_historys)
        paginated_payment_historys = self.paginate_queryset(payment_historys, request, view=self)

        subscription_plan = get_object_or_404(Subscription,
                                              payment_method=subscription.payment_method)
        future_payment = subscription_plan.subscription_type.price

        payment_history_serializer = PaymentHistorySerializer(paginated_payment_historys,
                                                              many=True)
        response_data = {"payment_history": payment_history_serializer.data}
        response_data["future_payment"] = {"price": future_payment,
                                           "date": subscription_plan.next_payment_date}

        return self.get_paginated_response(response_data)


class UpdateSubscription(UpdateAPIView):
    serializer_class = SubscriptionSerializer

    def get_object(self):
        return get_object_or_404(Subscription, pk=self.kwargs['pk'])

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class DeleteUpdateSubscription(APIView):
    permission_classes = [IsAuthenticated]

    def _get_billing_period_end(self, date):
        return date + relativedelta(days=-1)

    def get_object(self, pk):
        return get_object_or_404(Subscription, pk=pk)

    def patch(self, request, *args, **kwargs):
        """
        only allows patch of subscription type


        """
        orig_subscription = self.get_object(kwargs['pk'])
        new_subscription_type = request.data["subscription_type_id"]
        orig_subscription.subscription_type = new_subscription_type
        orig_subscription.save()
        serializer = SubscriptionSerializer(orig_subscription)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        orig_subscription = self.get_object(kwargs['pk'])
        orig_payment_date = orig_subscription.next_payment_date
        serializer = SubscriptionSerializer(orig_subscription, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        subscription = self.get_object(kwargs['pk'])

        billing_period_end = self._get_billing_period_end(subscription.next_payment_date)
        to_unenroll = ClassInstance.objects \
            .filter(userenroll__user__pk=subscription.user.id).filter(date__gt=billing_period_end)
        for class_instance in to_unenroll:
            class_instance.capacity_count -= 1

            class_instance.userenroll_set.all().delete()
            class_instance.save()
        subscription.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
        # drop classes


class SubscriptionDetail(APIView):
    permission_classes = [IsAuthenticated]

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
