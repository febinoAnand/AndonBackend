from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.

class SendReport(models.Model):
    date = models.DateField(null=False, blank=False)
    time = models.TimeField(null=False, blank=False)
    title = models.CharField(max_length=25)
    message = models.TextField(max_length=200)
    send_to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_reports', null=False, blank=False)
    users_group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='sent_group', null=False, blank=False)
    delivery_status = models.CharField(max_length=50, null=False, blank=False, default="Unknown")

class NotificationAuth(models.Model):
    user_to_auth = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False, related_name='user_name' )
    noti_token = models.TextField(max_length=50, null=False, blank=False)

class Setting(models.Model):
    application_id = models.TextField(max_length=50, null=False, blank=False)