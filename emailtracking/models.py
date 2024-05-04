from django.db import models
from django.db.models import JSONField
from django.contrib.auth.models import Group
import json
# Create your models here.

class Inbox(models.Model):
    date = models.DateField()
    time = models.TimeField()
    from_email = models.EmailField()
    to_email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    message_id = models.IntegerField(null=True)

    def __str__(self):
        return self.subject

class Ticket(models.Model):
    ticketname = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    inboxMessage = models.OneToOneField(Inbox, on_delete=models.CASCADE)
    actual_json = JSONField(null=True)
    required_json = JSONField(null=True)
    log = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.ticketname

class Parameter(models.Model):
    CHARACTER = 'character'
    NUMBER = 'number'
    DATATYPE_CHOICES = [
        (CHARACTER, 'Character'),
        (NUMBER, 'Number'),
    ]
    alias = models.CharField(max_length=15, blank=False, null=False)
    field = models.CharField(max_length=30, unique=True, blank=False, null=False)
    datatype = models.CharField(max_length=15, blank=False, null=False, choices=DATATYPE_CHOICES)

    def __str__(self):
        return self.alias
    
class ParameterFilter(models.Model):
    GREATER_THAN = 'greater than'
    LESS_THAN = 'less than'
    EQUALS = 'equals'
    NOT_EQUALS = 'not equals'
    IS_EXIST = 'is exist'

    OPERATOR_CHOICES = [
        (GREATER_THAN, 'Greater than'),
        (LESS_THAN, 'Less than'),
        (EQUALS, 'Equals'),
        (NOT_EQUALS, 'Not Equals'),
        (IS_EXIST, 'Is Exist'),
    ]

    operator = models.CharField(max_length=20, choices=OPERATOR_CHOICES)
    value = models.CharField(max_length=50)

    def __str__(self):
        return self.value

class Trigger(models.Model):
    trigger_name = models.CharField(max_length=255, blank=False, null=False)
    trigger_field = models.ForeignKey(Parameter, on_delete=models.CASCADE, blank=False, null=False)
    parameter_filter_list = models.ManyToManyField(ParameterFilter, blank=False, related_name="parameter_filter_lists")
    group_to_send = models.ForeignKey(Group, on_delete=models.SET_NULL, blank=True, null=True)
    notification_message = models.TextField(blank=True, null=True)
    trigger_switch = models.BooleanField(default=False)
    send_sms = models.BooleanField(default=False)
    send_notification = models.BooleanField(default=False)

    def __str__(self):
        return self.trigger_name

class Setting(models.Model):
    host = models.CharField(max_length=100, default='default_host')
    port = models.IntegerField(default=8080)
    username = models.CharField(max_length=100, default='default_username')
    password = models.CharField(max_length=100, default='default_password')
    checkstatus = models.BooleanField(default=False)
    checkinterval = models.IntegerField(default=60)
    phone = models.CharField(max_length=15, default='0000000000')
    sid = models.CharField(max_length=100, default='default_sid')
    auth_token = models.CharField(max_length=100, default='default_auth_token')

    def save(self, *args, **kwargs):
        if not self.pk and Setting.objects.exists():
            raise ValueError("Only one instance of Settings can be created")
        return super().save(*args, **kwargs)

    def __str__(self):
        return "Setting"