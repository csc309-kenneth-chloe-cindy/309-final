# Generated by Django 4.1.2 on 2022-11-15 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0003_alter_classinstance_class_offering_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeinterval',
            name='day',
            field=models.IntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')], max_length=1),
        ),
    ]
