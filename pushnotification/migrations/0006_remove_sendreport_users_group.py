# Generated by Django 4.2.4 on 2024-05-07 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pushnotification', '0005_alter_sendreport_delivery_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sendreport',
            name='users_group',
        ),
    ]