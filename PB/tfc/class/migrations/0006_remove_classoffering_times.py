# Generated by Django 4.1.3 on 2022-11-15 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('class', '0005_userenroll'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classoffering',
            name='times',
        ),
    ]