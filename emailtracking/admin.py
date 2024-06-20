from django.contrib import admin
from .models import *

# Register your models here.
class InboxAdmin(admin.ModelAdmin):
    list_display = ["date","time","from_email","to_email","subject","show_message"]
 
    def show_message(self,obj):
        return obj.message[:10]+"..."

admin.site.register(Inbox,InboxAdmin)

class TicketAdmin(admin.ModelAdmin):
    list_display = ["date","time","ticketname"]

    def parsed_from_message(self,obj):
        return obj.actual_json

    def selected_field(self,obj):
        return obj.required_json


admin.site.register(Ticket, TicketAdmin)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('dep_alias', 'department')
    search_fields = ('dep_alias', 'department')
    filter_horizontal = ('users_to_send',)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'Department', 'message', 'get_users_to_send')
    search_fields = ('Department', 'message')
    filter_horizontal = ('send_to_user',)

    def get_users_to_send(self, obj):
        return ", ".join([user.username for user in obj.users_to_send.all()])
    get_users_to_send.short_description = 'Users to Send'



class EmailIDAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'active']

admin.site.register(EmailID, EmailIDAdmin)