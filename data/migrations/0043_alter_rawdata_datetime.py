# Generated by Django 4.2.4 on 2024-05-07 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0042_alter_rawdata_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawdata',
            name='datetime',
            field=models.DateTimeField(default='2024-05-07 13:18:18', editable=False),
        ),
    ]
