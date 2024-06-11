from django.db import models
from django.core.validators import MaxLengthValidator
from twilio.rest import Client
from django.core.exceptions import ValidationError
from django.utils import timezone


# Create your models here.
class SMSNumber(models.Model):
    smsnumber = models.CharField(unique=True,max_length=20,null=False,blank=False)
    description = models.CharField(max_length=20,null=True,blank=True)

    def clean(self):
        if not "+" in self.smsnumber:
            raise ValidationError("Add country Code in the number")

    def __str__(self):
        return self.smsnumber

class Setting(models.Model):
    sid = models.CharField(max_length=100, default='default_sid')
    auth_token = models.CharField(max_length=100, default='default_auth_token')
    # number = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        if not self.pk and Setting.objects.exists():
            raise ValueError("Only one instance of Settings can be created")
        return super().save(*args, **kwargs)

    def __str__(self):
        return "Settings"



class SendReport(models.Model):
    date = models.DateField(null=True,blank=True)
    time = models.TimeField(null=True,blank=True)
    to_number = models.CharField(max_length=15, null=False, blank=False)
    from_number = models.ForeignKey(SMSNumber,null=False, blank=False,on_delete=models.SET("Number deleted.."))
    message = models.TextField(max_length=100, null=False, blank=False, validators=[MaxLengthValidator(100)])
    delivery_status = models.TextField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])

    def clean(self):
        if not "+" in self.to_number:
            raise ValidationError("Add country Code in the number")

    def save(self, *args, **kwargs):

        smsSettings = Setting.objects.all()[0]
        account_sid = smsSettings.sid
        auth_token = smsSettings.auth_token
        client = Client(account_sid, auth_token)
        self.date = timezone.now()
        self.time = timezone.now()
        # print (self.from_number.smsnumber)
        try:

            message = client.messages.create(
                from_=self.from_number.smsnumber,
                body=self.message,
                to=self.to_number
            )
            print(message.sid.status)
            self.delivery_status = message
        except Exception as e:
            self.delivery_status = e

        super(SendReport, self).save(*args, **kwargs)

