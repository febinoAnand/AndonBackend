# Generated by Django 4.2.4 on 2024-06-20 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailtracking', '0015_rename_dep_words_report_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default='2024-06-20 12:00:00'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='department',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
