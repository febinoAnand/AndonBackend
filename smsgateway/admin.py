from django.contrib import admin
from .models import *

# Register your models here.
class SendReportAdmin(admin.ModelAdmin):
    list_display = ["date","time","to_number","from_number","message","delivery_status"]

admin.site.register(SendReport, SendReportAdmin)


class SettingAdmin(admin.ModelAdmin):
    list_display = ["sid","auth_token","number"]

admin.site.register(Setting, SettingAdmin)