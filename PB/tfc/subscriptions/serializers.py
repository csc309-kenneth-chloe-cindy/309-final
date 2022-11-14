from .models import Subscription, SubscriptionPlan, PaymentMethod, PaymentHistory
from accounts.serializers import TFCUserSerializer
from rest_framework.fields import CurrentUserDefault
from rest_framework import serializers


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
    user = TFCUserSerializer(read_only=True)

    subscription_type_id = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        payment_method_data = validated_data.pop("payment_method")
        user = self.context.get("user")

        payment_method = PaymentMethod.objects.create(**payment_method_data)

        subscription = Subscription.objects.create(payment_method=payment_method, user=user,
                                                   **validated_data)
        return subscription

    class Meta:
        model = Subscription
        fields = ["subscription_type", "payment_method", "user", "subscription_type_id"]
