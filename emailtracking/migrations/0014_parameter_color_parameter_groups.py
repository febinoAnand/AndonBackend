# Generated by Django 4.2.4 on 2024-06-04 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailtracking', '0013_report_ticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='parameter',
            name='color',
            field=models.CharField(blank=True, max_length=7, null=True),
        ),
        migrations.AddField(
            model_name='parameter',
            name='groups',
            field=models.ManyToManyField(blank=True, to='emailtracking.parameter'),
        ),
    ]
