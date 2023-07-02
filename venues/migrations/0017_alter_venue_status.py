# Generated by Django 4.1.7 on 2023-07-02 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0016_alter_favouritevenues_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='status',
            field=models.CharField(blank=True, choices=[('active', 'Active'), ('suspended', 'Suspended')], default='suspended', max_length=10),
        ),
    ]