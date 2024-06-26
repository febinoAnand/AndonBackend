# Generated by Django 4.2.4 on 2023-08-26 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0004_alter_machine_image'),
        ('data', '0005_alter_lastproblemdata_issuetime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problemdata',
            name='acknowledgeTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='problemdata',
            name='endTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='problemdata',
            name='rfidTime',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='devices.rfid'),
        ),
    ]
