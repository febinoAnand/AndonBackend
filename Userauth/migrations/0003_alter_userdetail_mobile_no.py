# Generated by Django 4.2.4 on 2024-05-11 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Userauth', '0002_rename_settings_setting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetail',
            name='mobile_no',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
