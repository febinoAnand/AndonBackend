from django.contrib import admin
from .models import *

# Register your models here.
class SendReportAdmin(admin.ModelAdmin):
    list_display = ["date","time","title","message","send_to_user","delivery_status"]
    fields = ["date","time","title","message","send_to_user","users_group","delivery_status"]
    readonly_fields = ["delivery_status"]
    def has_change_permission(self, request, obj=None):
        return False
admin.site.register(SendReport, SendReportAdmin)

class NotificationAuthAdmin(admin.ModelAdmin):
    list_display = ("noti_token", "user_to_auth" ,)

admin.site.register(NotificationAuth, NotificationAuthAdmin)

class SettingAdmin(admin.ModelAdmin):
    list_display = ["application_name","application_id"]

    def has_add_permission(self, request):
        if len(Setting.objects.all()) > 0:
            return False
        return True

admin.site.register(Setting, SettingAdmin)