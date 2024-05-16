from django.contrib import admin
from django.http import HttpRequest
from .models import *
# Register your models here.

class UnauthUserAdmin(admin.ModelAdmin):
    list_display = ["mobile_no","createdatetime","otp","emailaddress","session_id","device_id","otp_called","designation","is_existing_user","verification_token"]

admin.site.register(UnauthUser, UnauthUserAdmin)

class UserDetailAdmin(admin.ModelAdmin):
    list_display = ["extUser","designation","mobile_no","device_id","auth_state","expiry_time"]

admin.site.register(UserDetail, UserDetailAdmin)

class SettingAdmin(admin.ModelAdmin):
    list_display = ["all_user_expiry_time","OTP_resend_interval","OTP_valid_time","OTP_call_count","OTP_wrong_count"]

    def has_add_permission(self, request) :
        if Setting.objects.count() > 0:
            return False
        return True

admin.site.register(Setting, SettingAdmin)