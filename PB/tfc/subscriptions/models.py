from django.db import models
from django.db.models import CASCADE

# # Create your models here.
MODEL_TYPES = (
    (0, "Yearly"),
    (1, "Monthly")
)


class SubscriptionPlan(models.Model):
    price = models.FloatField(null=False)
    period = models.IntegerField(choices=MODEL_TYPES)


class PaymentMethod(models.Model):
    card_number = models.PositiveIntegerField()
    security_code = models.PositiveIntegerField()


class PaymentHistory(models.Model):
    amount = models.PositiveIntegerField()
    payment_method = models.ForeignKey(to=PaymentMethod, on_delete=CASCADE)
    date_time = models.DateTimeField()


class Subscription(models.Model):
    payment_date = models.DateField()
    subscription_type = models.ForeignKey(to=SubscriptionPlan, on_delete=CASCADE)
    payment_method = models.ForeignKey(to=PaymentMethod, on_delete=CASCADE)
