from django.db import models
from django.db.models import JSONField
from django.contrib.auth.models import Group, User
import json
import random
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
    
    alias = models.CharField(max_length=30, blank=False, null=False)
    field = models.CharField(max_length=30, unique=True, blank=False, null=False)
    datatype = models.CharField(max_length=15, blank=False, null=False, choices=DATATYPE_CHOICES)
    color = models.CharField(max_length=7, blank=True, null=True)  
    groups = models.ManyToManyField(Group, blank=False)  

    class Meta:
        verbose_name = "field"
        verbose_name_plural = "fields"

    def __str__(self):
        return self.alias

    def save(self, *args, **kwargs):
        if not self.pk and not self.color:  
            self.color = self._generate_random_color()
        super().save(*args, **kwargs)

    def _generate_random_color(self):
        return "#{:06x}".format(random.randint(0, 0xFFFFFF))
    
class ParameterFilter(models.Model):
    GREATER_THAN_OR_EQUAL = 'greater than or equal'
    GREATER_THAN = 'greater than'
    LESS_THAN_OR_EQUAL = 'less than or equal'
    LESS_THAN = 'less than'
    EQUALS = 'equals'
    NOT_EQUALS = 'not equals'
    IS_EXIST = 'is exist'

    OPERATOR_CHOICES = [
        (GREATER_THAN_OR_EQUAL, 'Greater than or equal'),
        (GREATER_THAN, 'Greater than'),
        (LESS_THAN_OR_EQUAL, 'Less than or equal'),
        (LESS_THAN, 'Less than'),
        (EQUALS, 'Equals'),
        (NOT_EQUALS, 'Not Equals'),
        (IS_EXIST, 'Is Exist'),
    ]

    LOGICAL_OPERATOR_CHOICES = [
        ('AND', 'AND'),
        ('OR', 'OR'),
    ]

    operator = models.CharField(max_length=25, choices=OPERATOR_CHOICES)
    value = models.CharField(max_length=50)
    logical_operator = models.CharField(max_length=3, choices=LOGICAL_OPERATOR_CHOICES, default='AND')
    # trigger_fields = models.ForeignKey(Trigger,related_name="triggering_fields", on_delete=models.CASCADE,null=False,blank=False)

    def __str__(self):
        return f"{self.operator}-{self.value} ({self.logical_operator})"



class Trigger(models.Model):
    trigger_name = models.CharField(max_length=255, blank=False, null=False)
    trigger_field = models.ForeignKey(Parameter, on_delete=models.CASCADE, blank=False, null=False,related_name="trigger_field")
    parameter_filter_list = models.ManyToManyField(ParameterFilter, blank=False, related_name="parameter_filter_lists")
    users_to_send = models.ManyToManyField(User, blank=False, related_name="trigger_user")
    group_to_send = models.ForeignKey(Group, on_delete=models.CASCADE, blank=False, related_name="trigger_group")
    notification_message = models.TextField(blank=True, null=True)
    trigger_switch = models.BooleanField(default=False)
    send_sms = models.BooleanField(default=False)
    send_notification = models.BooleanField(default=False)


    def __str__(self):
        return self.trigger_name

    



class Report(models.Model):
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    active_trigger = models.ForeignKey(Trigger,null=False,blank=False,on_delete=models.CASCADE, related_name="report_trigger")
    actual_value = models.CharField(max_length=50,null=True,blank=True)
    ticket = models.ForeignKey(Ticket,null=True,blank=True,on_delete=models.DO_NOTHING)


class Setting(models.Model):
    host = models.CharField(max_length=100, default='default_host')
    port = models.IntegerField(default=8080)
    username = models.CharField(max_length=100, default='default_username')
    password = models.CharField(max_length=100, default='default_password')
    checkstatus = models.BooleanField(default=False)
    checkinterval = models.IntegerField(default=60)

    def save(self, *args, **kwargs):
        if not self.pk and Setting.objects.exists():
            raise ValueError("Only one instance of Settings can be created")
        return super().save(*args, **kwargs)

    def __str__(self):
        return "Setting"