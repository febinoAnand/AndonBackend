# Generated by Django 4.2.4 on 2024-05-11 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Userauth', '0006_setting_unauth_user_expiry_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unauthuser',
            name='device_id',
            field=models.CharField(max_length=50),
        ),
    ]
