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

class SearchParameter(models.Model):
    name = models.CharField(max_length=20)
    hunt_word = models.CharField(max_length=50, unique=True)
    message = models.CharField(max_length=250)
    mobile = models.CharField(max_length=10)
    country_code = models.CharField(max_length=3)

    def __str__(self):
        return self.name