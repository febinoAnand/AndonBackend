# Generated by Django 4.2.4 on 2024-06-20 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emailtracking', '0012_remove_report_active_trigger_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='log',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='required_json',
        ),
        migrations.DeleteModel(
            name='Trigger',
        ),
    ]