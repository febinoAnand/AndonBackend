# Generated by Django 4.2.4 on 2024-06-04 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0013_alter_user_email'),
        ('emailtracking', '0016_alter_parameter_groups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parameter',
            name='groups',
            field=models.ManyToManyField(blank=True, to='auth.group'),
        ),
    ]
