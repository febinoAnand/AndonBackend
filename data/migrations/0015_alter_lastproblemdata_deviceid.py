# Generated by Django 4.2.4 on 2023-10-15 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0005_rename_hmi_device'),
        ('data', '0014_problemdata_deviceid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lastproblemdata',
            name='deviceID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='devices.device'),
        ),
    ]
