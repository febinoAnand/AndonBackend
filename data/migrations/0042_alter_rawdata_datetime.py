from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0041_alter_rawdata_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawdata',
            name='datetime',
            field=models.DateTimeField(default='2024-05-07 16:09:57', editable=False),
        ),
    ]
