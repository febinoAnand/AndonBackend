# Generated by Django 4.2.4 on 2024-06-10 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailtracking', '0007_alter_trigger_group_to_send'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailid',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
