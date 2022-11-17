from django.db import models
from django.db.models import CASCADE
from accounts.models import TFCUser
import datetime
import dateutil.relativedelta as rd

# # Create your models here.
YEARLY = "Yearly"
MONTHLY = "Monthly"

MODEL_TYPES = (
    (0, YEARLY),
    (1, MONTHLY)
)


def get_period(num):
    if num == 0:
        return YEARLY
    else:
        return MONTHLY


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
    # subscription payment method is one subscription to one payment mehtods
    payment_method = models.ForeignKey(to=PaymentMethod, on_delete=CASCADE)
    # add user
    user = models.ForeignKey(to=TFCUser, on_delete=CASCADE)
    next_payment_date = models.DateField()

    def payment_due_today(self):
        return datetime.date.today() == self.next_payment_date
    def get_next_payment_date_from_date(self, date):
        period = get_period(self.subscription_type.period)
        if period == YEARLY:
            return date + rd.relativedelta(years=1)
        elif period == MONTHLY:
            return date + rd.relativedelta(months=1)
        return None
    def make_payment(self):
        today = datetime.date.today()
        payment_amount = self.subscription_type.price
        payment_history = PaymentHistory.objects.create(amount = payment_amount, payment_method = self.payment_method)
        payment_history.save()
        self.next_payment_date = self.get_next_payment_date_from_date(today)
        self.save()

def has_active_subscription(user_id):
    return Subscription.objects.filter(user=user_id).exists()
