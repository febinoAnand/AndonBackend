# Generated by Django 4.2.4 on 2024-06-04 22:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0013_alter_user_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inbox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('from_email', models.EmailField(max_length=254)),
                ('to_email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('message_id', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias', models.CharField(max_length=30)),
                ('field', models.CharField(max_length=30, unique=True)),
                ('datatype', models.CharField(choices=[('character', 'Character'), ('number', 'Number')], max_length=15)),
                ('color', models.CharField(blank=True, max_length=7, null=True)),
                ('groups', models.ManyToManyField(blank=True, to='auth.group')),
            ],
            options={
                'verbose_name': 'field',
                'verbose_name_plural': 'fields',
            },
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.CharField(default='default_host', max_length=100)),
                ('port', models.IntegerField(default=8080)),
                ('username', models.CharField(default='default_username', max_length=100)),
                ('password', models.CharField(default='default_password', max_length=100)),
                ('checkstatus', models.BooleanField(default=False)),
                ('checkinterval', models.IntegerField(default=60)),
            ],
        ),
        migrations.CreateModel(
            name='Trigger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trigger_name', models.CharField(max_length=255)),
                ('notification_message', models.TextField(blank=True, null=True)),
                ('trigger_switch', models.BooleanField(default=False)),
                ('send_sms', models.BooleanField(default=False)),
                ('send_notification', models.BooleanField(default=False)),
                ('group_to_send', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trigger_group', to='auth.group')),
                ('trigger_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trigger_field', to='emailtracking.parameter')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticketname', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('actual_json', models.JSONField(null=True)),
                ('required_json', models.JSONField(null=True)),
                ('log', models.TextField(blank=True, null=True)),
                ('inboxMessage', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='emailtracking.inbox')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('actual_value', models.CharField(blank=True, max_length=50, null=True)),
                ('active_trigger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_trigger', to='emailtracking.trigger')),
                ('ticket', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='emailtracking.ticket')),
            ],
        ),
        migrations.CreateModel(
            name='ParameterFilter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operator', models.CharField(choices=[('greater than or equal', 'Greater than or equal'), ('greater than', 'Greater than'), ('less than or equal', 'Less than or equal'), ('less than', 'Less than'), ('equals', 'Equals'), ('not equals', 'Not Equals'), ('is exist', 'Is Exist')], max_length=25)),
                ('value', models.CharField(max_length=50)),
                ('logical_operator', models.CharField(choices=[('AND', 'AND'), ('OR', 'OR')], default='AND', max_length=3)),
                ('trigger_fields', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='triggering_fields', to='emailtracking.trigger')),
            ],
        ),
    ]
