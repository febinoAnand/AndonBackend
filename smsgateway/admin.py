from django.contrib import admin
from django.http import HttpRequest
from .models import *

# Register your models here.
class SendReportAdmin(admin.ModelAdmin):
    list_display = ["date","time","to_number","message"]
    fields = ["date","time","to_number","from_number","message"]
    readonly_fields = ["date","time","delivery_status"]
    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(SendReport, SendReportAdmin)

class SMSNumberAdmin(admin.ModelAdmin):
    list_display = ("smsnumber","description")

admin.site.register(SMSNumber, SMSNumberAdmin)

class SettingAdmin(admin.ModelAdmin):
    list_display = ["sid","auth_token", "is_active"]
    def has_add_permission(self, request) :
        if Setting.objects.count() > 0:
            return False
        return True

admin.site.register(Setting, SettingAdmin)