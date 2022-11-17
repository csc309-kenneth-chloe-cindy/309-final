from django.core.management.base import BaseCommand, CommandError
from subscriptions.models import Subscription
import datetime
from subscriptions.serializers import SubscriptionSerializer


class Command(BaseCommand):
    help = "Checks for payments due today and makes them"

    def handle(self, *args, **options):
        today = datetime.date.today()
        to_pay = Subscription.objects.filter(next_payment_date=today)
        num_payments = 0
        for subscription in to_pay:
            num_payments += 1
            subscription.make_payment()

        self.stdout.write(f"Made {num_payments} payments")
