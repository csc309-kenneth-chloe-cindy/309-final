from django.db import models
from django.db.models import CASCADE

# # Create your models here.
# class SubscriptionPlan(models.Model):
#     price = models.FloatField(null=False)
#     period = models.CharField(max_length=200, null=False)
#
#     def __str__(self):
#         return self.name
#
# class Subscription(models.Model):
#     payment_date = models.CharField(max_length=200, null=False)
#     subscription_type = models.ForeignKey(to=SubscriptionPlan, on_delete=CASCADE, related_name='subscription_plan')
#     # payment_method = models.ForeignKey(to=PaymentMethod, on_delete=CASCADE, related_name='payment_method')
#
#     def __str__(self):
#         return self.name
#
# class PaymentMethod(models.Model):
#     card_number = models.CharField(max_length=200, null=False)
#     security_code = models.CharField(max_length=200, null=False)
#
#     def __str__(self):
#         return self.name
