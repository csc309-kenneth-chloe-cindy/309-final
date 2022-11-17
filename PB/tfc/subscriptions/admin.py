from django.contrib import admin
from .models import SubscriptionPlan, Subscription, PaymentHistory, PaymentMethod

# Register your models here.
admin.site.register(SubscriptionPlan)

# TODO: remove after done with TESTING
admin.site.register(Subscription)
admin.site.register(PaymentHistory)
