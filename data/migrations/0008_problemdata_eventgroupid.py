# Generated by Django 4.2.4 on 2023-08-27 04:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_alter_event_button_alter_event_indicator_and_more'),
        ('data', '0007_lastproblemdata_eventgroupid'),
    ]

    operations = [
        migrations.AddField(
            model_name='problemdata',
            name='eventGroupID',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='events.eventgroup'),
            preserve_default=False,
        ),
    ]
