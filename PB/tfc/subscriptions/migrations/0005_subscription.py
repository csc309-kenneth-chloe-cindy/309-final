# Generated by Django 4.1.3 on 2022-11-14 19:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('subscriptions', '0004_delete_subscription'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscriptions.paymentmethod')),
                ('subscription_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscriptions.subscriptionplan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
