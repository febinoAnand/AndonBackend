from django.db import models
from django.db.models import JSONField
from django.contrib.auth.models import Group, User
from django.utils import timezone
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
    is_satisfied = models.BooleanField(default=False)

    def __str__(self):
        return self.ticketname

    def is_ticket_satisfied(self):
        return self.is_satisfied
    
    def save(self, *args, **kwargs):
        if not self.date:
            self.date = timezone.now().date()
        if not self.time:
            self.time = timezone.now().time()
        super().save(*args, **kwargs)



class Report(models.Model):
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    Department = models.CharField(max_length=255, default="Default Dep Words")
    send_to_user = models.ManyToManyField(User, related_name='report')
    message = models.TextField(default="Default message")

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = timezone.now().date()
        if not self.time:
            self.time = timezone.now().time()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.department

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

class EmailID(models.Model):
    email = models.EmailField(unique=True)
    active = models.BooleanField(default=True)  

    def __str__(self):
        return self.email
    
class Department(models.Model):
    dep_alias = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    users_to_send = models.ManyToManyField(User, related_name='departments_to_send')
    date = models.DateTimeField(auto_now_add=True)
    time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.dep_alias