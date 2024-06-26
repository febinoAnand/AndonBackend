# Generated by Django 4.2.4 on 2024-05-07 16:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pushnotification', '0007_sendreport_users_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sendreport',
            name='send_to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notify_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
