# Generated by Django 3.2.20 on 2023-07-06 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0019_alter_venue_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='venuebooking',
            name='payment_id',
            field=models.CharField(default='rkektlmwertm', max_length=100),
            preserve_default=False,
        ),
    ]
