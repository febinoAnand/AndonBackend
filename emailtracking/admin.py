from django.contrib import admin
from .models import *

# Register your models here.
class InboxAdmin(admin.ModelAdmin):
    list_display = ["date","time","from_email","to_email","subject","message","message_id"]

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

class SettingsAdmin(admin.ModelAdmin):
    list_display = ["host","port","username","password","checkstatus","checkinterval","phone","sid","auth_token"]

admin.site.register(Settings, SettingsAdmin)