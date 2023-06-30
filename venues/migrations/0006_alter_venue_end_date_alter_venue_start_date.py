# Generated by Django 4.1.7 on 2023-06-22 17:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0005_alter_venue_end_date_alter_venue_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='venue',
            name='start_date',
            field=models.DateField(blank=True, default=datetime.datetime.now, null=True),
        ),
    ]
