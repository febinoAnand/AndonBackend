import uuid

import binascii
import os

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Device(models.Model):
    deviceID = models.CharField(max_length=15,blank=False,unique=True,default=uuid.uuid1)
    model = models.CharField(max_length=10)
    hardwareVersion = models.CharField(max_length=10)
    softwareVersion = models.CharField(max_length=10)
    # token = models.CharField(max_length=30)
    devicePassword = models.CharField(max_length=20)

    def __str__(self):
        return self.deviceID

class Machine(models.Model):
    machineID = models.CharField(max_length=15,unique=True, blank=False, default=uuid.uuid1)
    name = models.CharField(max_length=50,blank=False)
    manufacture = models.CharField(max_length=50)
    model = models.CharField(max_length=10)
    line = models.CharField(max_length=10)
    image = models.ImageField(upload_to='images/machineimages',blank=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    def __str__(self):
        return self.machineID

class RFID(models.Model):
    rfid = models.CharField(max_length=50,blank=False,unique=True,default=uuid.uuid1)
    rfidUser = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.rfid


class UnRegisteredDevice(models.Model):
    sessionID = models.UUIDField(blank=False,null=False)
    deviceID = models.CharField(max_length=15,blank=False,unique=True,default=uuid.uuid1)
    model = models.CharField(max_length=10,blank=True,null=True)
    hardwareVersion = models.CharField(max_length=10,blank=True,null=True)
    softwareVersion = models.CharField(max_length=10,blank=True,null=True)
    devicePassword = models.CharField(max_length=20)
    OTP = models.IntegerField(null=True,blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

class Token(models.Model):
    deviceID = models.OneToOneField(Device,blank=False,null=False,on_delete=models.CASCADE,related_name="deviceToken")
    token = models.CharField(max_length=30)
    createdAt = models.DateTimeField(auto_now_add=True)

# class Token(models.Model):
#     """
#     The default authorization token model.
#     """
#     key = models.CharField(_("Key"), max_length=40, primary_key=True)
#
#     deviceID = models.OneToOneField(
#         Device, related_name='auth_token',
#         on_delete=models.CASCADE, verbose_name="Device"
#     )
#     created = models.DateTimeField(_("Created"), auto_now_add=True)
#
#     class Meta:
#         verbose_name = _("Token")
#         verbose_name_plural = _("Tokens")
#
#     def save(self, *args, **kwargs):
#         if not self.key:
#             self.key = self.generate_key()
#         return super(Token, self).save(*args, **kwargs)
#
#     def generate_key(self):
#         return binascii.hexlify(os.urandom(20)).decode()
#
#     def __str__(self):
#         return self.key
