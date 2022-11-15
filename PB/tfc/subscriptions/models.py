from django.db import models
from django.db.models import CASCADE
from accounts.models import TFCUser

# # Create your models here.
MODEL_TYPES = (
    (0, "Yearly"),
    (1, "Monthly")
)
def get_period(num):
    if num == 0:
        return "Yearly"
    else:
        return "Monthly"


class SubscriptionPlan(models.Model):
    price = models.FloatField(null=False)
    period = models.IntegerField(choices=MODEL_TYPES)

    def __str__(self):
        if self.period == 0:
            return f"price: {self.price}, period: yearly"
        if self.period == 1:
            return f"price: {self.price}, period: monthly"


class PaymentMethod(models.Model):
    card_number = models.PositiveIntegerField()
    security_code = models.PositiveIntegerField()


class PaymentHistory(models.Model):
    amount = models.PositiveIntegerField()
    payment_method = models.ForeignKey(to=PaymentMethod, on_delete=CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)


class Subscription(models.Model):
    # subscription type is one subscription type to many subscriptions
    subscription_type = models.ForeignKey(to=SubscriptionPlan, on_delete=CASCADE)
    # subscription payment method is one subscription to many payment mehtods
    payment_method = models.ForeignKey(to=PaymentMethod, on_delete=CASCADE)
    # add user
    user = models.ForeignKey(to=TFCUser, on_delete=CASCADE)
    next_payment_date = models.DateField()
