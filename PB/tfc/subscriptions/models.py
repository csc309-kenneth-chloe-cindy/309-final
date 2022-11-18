from django.db import models
from django.db.models import CASCADE
from accounts.models import TFCUser
import datetime
import dateutil.relativedelta as rd
from django.shortcuts import get_object_or_404

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
            return f"price: {self.price}, period: yearly, pk: {self.pk}"
        if self.period == 1:
            return f"price: {self.price}, period: monthly, pk: {self.pk}"


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
    payment_method = models.OneToOneField(to=PaymentMethod, on_delete=CASCADE)
    # add user
    user = models.ForeignKey(to=TFCUser, on_delete=CASCADE)
    next_payment_date = models.DateField()

    def get_billing_period_end(self):
        return self.next_payment_date + rd.relativedelta(days=-1)

    def payment_due_today(self):
        return datetime.date.today() == self.next_payment_date

    def get_next_payment_date_from_date(self, date, period):
        if period == YEARLY:
            return date + rd.relativedelta(years=1)
        elif period == MONTHLY:
            return date + rd.relativedelta(months=1)
        return None

    def get_next_payment_date_with_altered_plan(self, new_period, old_period):
        if new_period == old_period:
            return self.next_payment_date
        last_payment_date = self.next_payment_date
        if old_period == YEARLY:
            last_payment_date = last_payment_date + rd.relativedelta(years=-1)
        elif old_period == MONTHLY:
            last_payment_date = last_payment_date + rd.relativedelta(months=-1)
        else:
            return None
        return self.get_next_payment_date_from_date(last_payment_date, new_period)

    def make_payment(self):
        today = datetime.date.today()
        payment_amount = self.subscription_type.price
        payment_history = PaymentHistory.objects.create(amount=payment_amount,
                                                        payment_method=self.payment_method)
        payment_history.save()
        period = get_period(self.subscription_type.period)
        self.next_payment_date = self.get_next_payment_date_from_date(today, period)
        self.save()

    def change_subscription_type(self, new_subscription_plan_id):
        new_subscription_type = get_object_or_404(SubscriptionPlan,
                                                  pk=new_subscription_plan_id)
        orig_period = get_period(self.subscription_type.period)
        new_period = get_period(new_subscription_type.period)
        if new_period == orig_period:
            print("NEW PERIOD IS SAME AS OLD")
            return self
        print("NEW PERIOD IS DIFF")
        self.subscription_type = new_subscription_type
        next_payment = self.get_next_payment_date_with_altered_plan(new_period, orig_period)
        self.next_payment_date = next_payment
        self.save()
        return self


def has_active_subscription(user_id):
    return Subscription.objects.filter(user=user_id).exists()
