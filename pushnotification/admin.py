from django.contrib import admin
from .models import *

# Register your models here.
class SendReportAdmin(admin.ModelAdmin):
    list_display = ["date","time","title","message","send_to_user","users_group","delivery_status"]

admin.site.register(SendReport, SendReportAdmin)

class NotificationAuthAdmin(admin.ModelAdmin):
    list_display = ("noti_token", "user_to_auth" ,)

admin.site.register(NotificationAuth, NotificationAuthAdmin)

class SettingAdmin(admin.ModelAdmin):
    list_display = ["application_id"]

admin.site.register(Setting, SettingAdmin)