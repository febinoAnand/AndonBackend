from django.contrib import admin
from .models import *

# Register your models here.
class InboxAdmin(admin.ModelAdmin):
    list_display = ["date","time","from_email","to_email","subject","show_message"]
    # def has_add_permission(self, request):
    #     return False

    def show_message(self,obj):
        return obj.message[:10]+"..."

admin.site.register(Inbox,InboxAdmin)

class TicketAdmin(admin.ModelAdmin):
    list_display = ["date","time","ticketname","selected_field"]

    def parsed_from_message(self,obj):
        return obj.actual_json

    def selected_field(self,obj):
        return obj.required_json


admin.site.register(Ticket, TicketAdmin)

class ParameterAdmin(admin.ModelAdmin):
    list_display = ["alias","field","datatype"]
    fields = ["alias","field","datatype","groups"]
    

admin.site.register(Parameter, ParameterAdmin)

class ParameterFilterAdmin(admin.ModelAdmin):
    list_display = ["logical_operator","operator","value"]

admin.site.register(ParameterFilter,ParameterFilterAdmin)

class TriggerAdmin(admin.ModelAdmin):
    list_display = ["trigger_name","field","group_to_send","notification_message","trigger_switch","send_sms","send_notification"]

    def field(self,obj):
        return obj.trigger_field.field

    # list_filter = ["trigger_name","trigger_field","group_to_send","notification_message","trigger_switch","send_sms","send_notification"]

admin.site.register(Trigger, TriggerAdmin)

class SettingAdmin(admin.ModelAdmin):

    list_display = ["host","port","username","password","checkstatus","checkinterval"]
    fields = ["host","port","username","password","checkstatus","checkinterval"]

    def has_add_permission(self, request):
        if len(Setting.objects.all()) > 0:
            return False
        return True

admin.site.register(Setting, SettingAdmin)

class ReportAdmin(admin.ModelAdmin):
    list_display = ('date','time','field_Word','actual_value','sent_group','trigger_message')

    # def has_add_permission(self, request):
    #     return False

    def has_change_permission(self, request, obj=None):
        return False

    def trigger_name(self,obj):
        if obj.active_trigger:
            return obj.active_trigger.trigger_name
        else:
            return 'NA'

    def field_Word(self, obj):
        if obj.active_trigger:
            return obj.active_trigger.trigger_field
        else:
            return 'NA'

    # def trigger_filter(self, obj):
    #     if obj.active_trigger:
    #         list_filter = [item for item in obj.active_trigger.parameter_filter_list.all()]
            # for item in obj.active_trigger.parameter_filter_list.all():
# 
            # return list_filter
        # else:
        #     return 'NA'

    def sent_group(self, obj):
        if obj.active_trigger:
            return obj.active_trigger.group_to_send
        else:
            return 'NA'

    def trigger_message(self, obj):
        if obj.active_trigger:
            return obj.active_trigger.notification_message
        else:
            return 'NA'

admin.site.register(Report,ReportAdmin)


    


@admin.register(EmailID)
class EmailIDAdmin(admin.ModelAdmin):
    list_display = ['email', 'setting']
    search_fields = ['email']