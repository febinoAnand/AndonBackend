from django.contrib import admin
from .models import *

# Register your models here.

class InboxAdmin(admin.ModelAdmin):
    list_display = ["date","time","from_email","to_email","subject","message","message_id"]

admin.site.register(Inbox,InboxAdmin)

class SettingsAdmin(admin.ModelAdmin):
    list_display = ["host","port","username","password","checkstatus","checkinterval","phone","sid","auth_token"]

admin.site.register(Settings,SettingsAdmin)

class SearchParameterAdmin(admin.ModelAdmin):
    list_display = ["name","hunt_word","message","user_group"]

admin.site.register(SearchParameter,SearchParameterAdmin)

class UserEmailTrackingAdmin(admin.ModelAdmin):
    list_display = ["user","designation","mobile"]

admin.site.register(UserEmailTracking,UserEmailTrackingAdmin)

class GroupAdmin(admin.ModelAdmin):
    list_display = ["pk","user_group"]
admin.site.register(GroupEmailTracking,GroupAdmin)