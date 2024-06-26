# Generated by Django 4.2.4 on 2023-12-01 14:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0019_alter_machine_machineid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rfid',
            name='rfid',
            field=models.CharField(default=uuid.uuid1, max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='unregistereddevice',
            name='deviceID',
            field=models.CharField(default=uuid.uuid1, max_length=15, unique=True),
        ),
    ]
