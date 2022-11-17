from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from .models import Subscription, SubscriptionPlan, PaymentMethod, PaymentHistory, \
    has_active_subscription
from classes.models import ClassInstance
from django.shortcuts import get_list_or_404, get_object_or_404
from .serializers import SubscriptionSerializer, PaymentHistorySerializer, PaymentMethodSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination


def cancel_user_subscription(user):
    subscription = get_object_or_404(Subscription, user=user)
    billing_period_end = subscription.get_billing_period_end()
    to_unenroll = ClassInstance.objects \
        .filter(userenroll__user__pk=user.id).filter(date__gt=billing_period_end)
    for class_instance in to_unenroll:
        try:
            class_instance.unenroll_user(user)
        except Exception as error:
            print(error)
    return subscription.delete()


# Create your views here.


class UpdatePaymentMethodView(UpdateAPIView):
    serializer_class = PaymentMethodSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(PaymentMethod, subscription__user=self.request.user)


class GetPaymentHistory(APIView, LimitOffsetPagination):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = self.request.user
        subscription = get_object_or_404(Subscription, user=user_id)

        payment_historys = get_list_or_404(PaymentHistory,
                                           payment_method=subscription.payment_method.id)
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


class SubscriptionDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Subscription, pk=pk)

    def patch(self, request, *args, **kwargs):
        """
        only allows patch of subscription type


        """
        orig_subscription = get_object_or_404(Subscription, user=request.user)
        new_subscription_type_id = request.data["subscription_type_id"]
        altered_subscription = orig_subscription.change_subscription_type(new_subscription_type_id)
        serializer = SubscriptionSerializer(altered_subscription)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        delete_result = cancel_user_subscription(request.user)

        return Response(delete_result, status=status.HTTP_200_OK)
        # drop classes

    def post(self, request, *args, **kwargs):
        if has_active_subscription(request.user.id):
            return Response({"Message": "User already has active subscription"},
                            status=status.HTTP_409_CONFLICT)
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
