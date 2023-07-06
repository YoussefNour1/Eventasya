# Generated by Django 3.2.20 on 2023-07-06 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_alter_eventbooking_total_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventbooking',
            name='ticket',
        ),
        migrations.AddField(
            model_name='eventbooking',
            name='ticket_price',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventbooking',
            name='ticket_type',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
