# Generated by Django 3.2.20 on 2023-07-05 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0018_venue_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='category',
            field=models.CharField(choices=[('religious', 'Religious'), ('openair', 'Open Air'), ('yacht', 'Yacht'), ('conference', 'Conference'), ('closed hall', 'Closed Hall')], max_length=20),
        ),
    ]
