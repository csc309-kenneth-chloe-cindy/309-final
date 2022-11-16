from django.contrib import admin
from .models import SubscriptionPlan, Subscription, PaymentHistory, PaymentMethod

# Register your models here.
admin.site.register(SubscriptionPlan)

# TESTING
admin.site.register(Subscription)
