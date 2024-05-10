from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0034_alter_rawdata_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawdata',
            name='datetime',
            field=models.DateTimeField(default='2024-05-07 15:31:37', editable=False),
        ),
    ]
