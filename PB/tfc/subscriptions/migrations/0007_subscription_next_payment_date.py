# Generated by Django 4.1.3 on 2022-11-15 03:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0006_alter_paymenthistory_date_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='next_payment_date',
            field=models.DateField(default=datetime.date(2022, 11, 15)),
            preserve_default=False,
        ),
    ]