from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0032_alter_rawdata_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawdata',
            name='datetime',
            field=models.DateTimeField(default='2024-05-03 18:54:13', editable=False),

        ),
    ]
