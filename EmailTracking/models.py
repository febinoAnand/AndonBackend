from django.db import models
from django.contrib.auth.models import User, Group
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

class Settings(models.Model):
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
        if not self.pk and Settings.objects.exists():
            raise ValueError("Only one instance of Settings can be created")
        return super().save(*args, **kwargs)

    def __str__(self):
        return "Settings"

class SearchParameter(models.Model):
    name = models.CharField(max_length=20)
    hunt_word = models.CharField(max_length=50, unique=True)
    message = models.CharField(max_length=250)
    user_group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
    
class UserEmailTracking(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation =models.CharField(max_length=25)
    mobile = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username

class GroupEmailTracking(models.Model):
    user_group = models.OneToOneField(Group, on_delete=models.CASCADE)
    user_list = models.ManyToManyField(User, related_name='groupemail')

    def __str__(self):
        return str(self.user_group)