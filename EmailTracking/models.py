from django.db import models

# Create your models here.

class Inbox(models.Model):
    date = models.DateField()
    time = models.TimeField()
    from_email = models.EmailField()
    to_email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.subject

from django.db import models

class Settings(models.Model):
    host = models.CharField(max_length=100, default='default_host')
    port = models.IntegerField(default=8080)
    username = models.CharField(max_length=100, default='default_username')
    password = models.CharField(max_length=100, default='default_password')
    checkstatus = models.BooleanField(default=False)
    checkinterval = models.IntegerField(default=60)

    def save(self, *args, **kwargs):
        if not self.pk and Settings.objects.exists():
            raise ValueError("Only one instance of Settings can be created")
        return super().save(*args, **kwargs)

    def __str__(self):
        return "Settings"
