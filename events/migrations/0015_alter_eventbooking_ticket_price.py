# Generated by Django 3.2.20 on 2023-07-06 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_auto_20230707_0046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventbooking',
            name='ticket_price',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]