# Generated by Django 4.2.4 on 2024-05-07 12:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smsgateway', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sendreport',
            name='delivery_status',
            field=models.TextField(blank=True, max_length=100, null=True, validators=[django.core.validators.MaxLengthValidator(100)]),
        ),
    ]
