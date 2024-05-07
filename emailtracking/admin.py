from django.contrib import admin
from .models import *

# Register your models here.
class InboxAdmin(admin.ModelAdmin):
    list_display = ["date","time","from_email","to_email","subject","message","message_id"]
    def has_add_permission(self, request):
        return False

admin.site.register(Inbox,InboxAdmin)

class TicketAdmin(admin.ModelAdmin):
    list_display = ["ticketname","date","time","inboxMessage","actual_json","required_json","log"]

admin.site.register(Ticket, TicketAdmin)

class ParameterAdmin(admin.ModelAdmin):
    list_display = ["alias","field","datatype"]

admin.site.register(Parameter, ParameterAdmin)

class ParameterFilterAdmin(admin.ModelAdmin):
    list_display = ["operator","value"]

admin.site.register(ParameterFilter,ParameterFilterAdmin)

class TriggerAdmin(admin.ModelAdmin):
    list_display = ["trigger_name","trigger_field","group_to_send","notification_message","trigger_switch","send_sms","send_notification"]

admin.site.register(Trigger, TriggerAdmin)

class SettingAdmin(admin.ModelAdmin):

    list_display = ["host","port","username","password","checkstatus","checkinterval"]

    def has_add_permission(self, request):
        if len(Setting.objects.all()) > 0:
            return False
        return True

admin.site.register(Setting, SettingAdmin)