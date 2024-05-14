# Generated by Django 4.2.4 on 2024-05-07 14:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pushnotification', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='application_name',
            field=models.CharField(default='NA', max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notificationauth',
            name='user_to_auth',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_name', to=settings.AUTH_USER_MODEL),
        ),
    ]