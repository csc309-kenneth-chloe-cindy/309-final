# Generated by Django 4.1.3 on 2022-11-14 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('studios', '0002_delete_studioimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudioImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='studio-images')),
                ('studio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='studio_images', to='studios.studio')),
            ],
        ),
    ]
