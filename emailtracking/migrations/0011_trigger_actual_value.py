# Generated by Django 4.2.4 on 2024-05-08 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailtracking', '0010_alter_trigger_group_to_send'),
    ]

    operations = [
        migrations.AddField(
            model_name='trigger',
            name='actual_value',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]