from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class UnauthUser(models.Model):
    mobile_no = models.CharField(max_length=15, null=False, blank=False)
    createdatetime = models.DateTimeField(auto_now_add=True)
    otp = models.DecimalField(max_digits=5, decimal_places=0, null=True, blank=True)
    emailaddress = models.EmailField(null=False, blank=False)
    session_id = models.UUIDField(default=uuid.uuid4, unique=True, null=False, blank=False)
    device_id = models.CharField(max_length=50, unique=True, null=False, blank=False)
    otp_called = models.IntegerField(default=0, null=False, blank=False)
    designation = models.CharField(max_length=15, null=True, blank=False)
    is_existing_user = models.BooleanField(default=False, null=False, blank=False)
    verification_token = models.UUIDField(default=uuid.uuid4, unique=True, null=True, blank=True)

class UserDetail(models.Model):
    extUser = models.OneToOneField(User, on_delete=models.CASCADE, related_name='extraUserDetails')
    designation = models.CharField(max_length=15, null=True, blank=False)
    mobile_no = models.CharField(max_length=15, null=False, blank=False)
    device_id = models.CharField(max_length=50, unique=True, null=False, blank=False)
    auth_state = models.IntegerField(default=0, null=False, blank=False)
    expiry_time = models.IntegerField(default =86400, null=False, blank=False)

class Setting(models.Model):
    all_user_expiry_time = models.IntegerField(default =86400, null=False, blank=False)
    OTP_resend_interval = models.IntegerField(default =20, null=False, blank=False)
    OTP_valid_time = models.IntegerField(default =600, null=False, blank=False)
    OTP_call_count = models.IntegerField(default =5, null=False, blank=False)
    OTP_wrong_count = models.IntegerField(default =3, null=False, blank=False)