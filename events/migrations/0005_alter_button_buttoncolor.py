# Generated by Django 4.2.4 on 2023-08-26 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_alter_button_buttonid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='button',
            name='buttonColor',
            field=models.CharField(max_length=7),
        ),
    ]
