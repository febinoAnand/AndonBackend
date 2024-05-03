from django.db import models
from django.core.validators import MaxLengthValidator

# Create your models here.

class SendReport(models.Model):
    date = models.DateField()
    time = models.TimeField()
    to_number = models.CharField(max_length=15, null=False, blank=False)
    from_number = models.CharField(max_length=15, null=False, blank=False)
    message = models.TextField(max_length=100, null=False, blank=False, validators=[MaxLengthValidator(100)])
    delivery_status = models.TextField(max_length=100, null=True, validators=[MaxLengthValidator(100)])


class Setting(models.Model):
    sid = models.CharField(max_length=100, default='default_sid')
    auth_token = models.CharField(max_length=100, default='default_auth_token')
    number = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        if not self.pk and Setting.objects.exists():
            raise ValueError("Only one instance of Settings can be created")
        return super().save(*args, **kwargs)

    def __str__(self):
        return "Settings"