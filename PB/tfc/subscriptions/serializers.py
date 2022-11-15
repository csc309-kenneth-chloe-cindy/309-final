from .models import Subscription, SubscriptionPlan, PaymentMethod, PaymentHistory
from accounts.serializers import TFCUserSerializer
from rest_framework.fields import CurrentUserDefault
from rest_framework import serializers
import datetime
from dateutil.relativedelta import relativedelta
from django.shortcuts import get_object_or_404


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ["price", "period"]


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ["card_number", "security_code"]


class PaymentHistorySerializer(serializers.ModelSerializer):
    payment_method = PaymentMethodSerializer(read_only=True)
    payment_method_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = PaymentHistory
        fields = ["amount", "date_time", "payment_method", "payment_method_id"]


class SubscriptionSerializer(serializers.ModelSerializer):
    subscription_type = SubscriptionPlanSerializer(read_only=True)
    payment_method = PaymentMethodSerializer()

    subscription_type_id = serializers.IntegerField(write_only=True)




    def create(self, validated_data):
        payment_method_data = validated_data.pop("payment_method")
        user = self.context.get("user")

        payment_method = PaymentMethod.objects.create(**payment_method_data)
        subscription_type_id = validated_data["subscription_type_id"]
        subscription_type = get_object_or_404(SubscriptionPlan, pk=subscription_type_id).period

        last_payment_date = datetime.date.today()
        next_payment_date = None
        if subscription_type == 0:
            # yearly
            next_payment_date = last_payment_date + relativedelta(years=1)
            print("with year jump: ", next_payment_date)
        elif subscription_type == 1:
            # monthly
            next_payment_date = last_payment_date + relativedelta(months=1)
            print("with month jump: ", next_payment_date)

        subscription = Subscription.objects.create(payment_method=payment_method, user=user,
                                                   next_payment_date=next_payment_date,
                                                   **validated_data)
        return subscription

    class Meta:
        model = Subscription
        fields = ["subscription_type", "payment_method", "subscription_type_id"]
