# Generated by Django 3.2.20 on 2023-07-07 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0021_remove_venuebooking_event_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venuebooking',
            name='request_status',
        ),
    ]