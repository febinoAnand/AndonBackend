from django.db import models
from django.contrib.auth.models import User, Group
import requests
import json

# Create your models here.

class SendReport(models.Model):
    date = models.DateField(null=False, blank=False)
    time = models.TimeField(null=False, blank=False)
    title = models.CharField(max_length=25)
    message = models.TextField(max_length=200)
    send_to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notify_user', null=False, blank=False)
    users_group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='sent_group',null=True,blank=True)
    delivery_status = models.CharField(max_length=50, null=False, blank=False, default="-")

    def save(self,*args,**kwargs):
        message = {
            "to": self.send_to_user.user_name.noti_token,
            "sound" : "default",
            "title":self.title,
            "priority":"high",
            "body": self.message
        }


        header = {
            "host": "exp.host",
            "accept": "application/json",
            "accept-encoding": "gzip, deflate",
            "content-type": "application/json"
        }
        print (message)
        response = requests.post("https://exp.host/--/api/v2/push/send",data=json.dumps(message),headers=header)
        print (response.status_code,response.reason)
        self.delivery_status = "{status} - {res}".format(status= response.status_code, res = response.reason)

        super(SendReport,self).save(*args,**kwargs)


class NotificationAuth(models.Model):
    user_to_auth = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False, related_name='user_name' )
    noti_token = models.CharField(max_length=50, null=False, blank=False)

class Setting(models.Model):
    application_name = models.CharField(max_length=30,null=False, blank=False)
    application_id = models.CharField(max_length=50, null=False, blank=False)

    def save(self, *args, **kwargs):
        if not self.pk and Setting.objects.exists():
            raise ValueError("Only one instance of Settings can be created")
        return super().save(*args, **kwargs)