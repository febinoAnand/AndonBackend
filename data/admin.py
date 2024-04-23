from django.contrib import admin
from .models import RawData,ProblemData,LastProblemData

# Register your models here.
class RawDataAdmin(admin.ModelAdmin):
    list_display = ["datetime", "data"]
    readonly_fields = ['datetime','data',]
    fields = ['datetime','data']

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False


class ProblemDataAdmin(admin.ModelAdmin):
    list_display = ["dateTimeNow","eventID","eventGroupID","machineID","issueTime","acknowledgeTime","endTime"]
    fields = ["dateTimeNow","date","time","eventID","eventGroupID","machineID","deviceID","issueTime","acknowledgeTime","endTime"]
    readonly_fields = ["dateTimeNow"]

    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False


class LastProblemDataAdmin(admin.ModelAdmin):
    list_display = ["dateTimeNow","eventID","eventGroupID","machineID","issueTime","acknowledgeTime","endTime"]
    fields = ["dateTimeNow","date","time","eventID","eventGroupID","machineID","deviceID","issueTime","acknowledgeTime","endTime"]
    readonly_fields = ["dateTimeNow"]

    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(RawData,RawDataAdmin)
admin.site.register(ProblemData,ProblemDataAdmin)
admin.site.register(LastProblemData,LastProblemDataAdmin)