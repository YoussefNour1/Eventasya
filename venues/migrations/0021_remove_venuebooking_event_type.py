# Generated by Django 3.2.20 on 2023-07-07 01:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0020_venuebooking_payment_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venuebooking',
            name='event_type',
        ),
    ]
