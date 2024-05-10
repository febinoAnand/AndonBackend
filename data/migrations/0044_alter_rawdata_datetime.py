from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0043_alter_rawdata_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawdata',
            name='datetime',

            field=models.DateTimeField(default='2024-05-07 13:19:42', editable=False),
        ),
    ]
