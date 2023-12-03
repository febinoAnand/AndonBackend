from django.contrib import admin
from .models import *

# Register your models here.

# admin.site.register(Token)

class DeviceAdmin(admin.ModelAdmin):
    list_display = ["deviceID","model","hardwareVersion","softwareVersion"]
    readonly_fields = ["deviceID"]
    def has_add_permission(self, request):
        return False

admin.site.register(Device,DeviceAdmin)


class MachineAdmin(admin.ModelAdmin):
    list_display = ["machineID","name","manufacture","model","line"]
admin.site.register(Machine,MachineAdmin)

# class RFIDAdmin(admin.ModelAdmin):
#     list_display = ["rfid","rfidUser"]
# admin.site.register(RFID,RFIDAdmin)

class UnRegisteredDeviceAdmin(admin.ModelAdmin):
    list_display = ["sessionID","deviceID","model","OTP","createdAt"]
    fields = ["sessionID","deviceID","devicePassword","model","hardwareVersion","softwareVersion","OTP","createdAt"]
    readonly_fields = ["createdAt","OTP","sessionID","deviceID"]

    def has_add_permission(self, request):
        return False

admin.site.register(UnRegisteredDevice,UnRegisteredDeviceAdmin)


class TokenAdmin(admin.ModelAdmin):
    list_display = ["deviceID","token","createdAt"]
    fields = ["deviceID","token","createdAt"]
    readonly_fields = ["createdAt"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(Token, TokenAdmin)



