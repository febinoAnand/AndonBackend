# Generated by Django 4.2.4 on 2024-06-04 10:57

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0013_alter_user_email'),
        ('Userauth', '0008_unauthuser_otp_wrong_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.group')),
            ],
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
    ]
