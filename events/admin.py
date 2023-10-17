from django.contrib import admin
from .models import *
# Register your models here.

# admin.site.register(Event)
# admin.site.register(Button)
# admin.site.register(Indicator)


class EventAdmin(admin.ModelAdmin):
    list_display = ["eventID","Button","Problem","Indicator"]
    fields = ["eventID","button","problem","indicator"]


@admin.register(Button)
class ButtonAdmin(admin.ModelAdmin):
    list_display = ["buttonID","buttonName","buttonColorName","buttonColor"]
    # list_display = [field.name for field in Button._meta.get_fields()]
    # list_display = admin.ModelAdmin._meta.get_all_field_names()


class ProblemCodeAdmin(admin.ModelAdmin):
    list_display = ["problemCode","problemName","problemDescription","problemType"]
admin.site.register(ProblemCode,ProblemCodeAdmin)


@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    list_display = ["indicatorID","indicatorpin","indicatorColor","indicatorColorName"]
    # list_display = [field.name for field in Indicator._meta.get_fields()]

class EventGroupAdmin(admin.ModelAdmin):
    list_display = ["groupID","groupName","selectedEvents"]

admin.site.register(EventGroup,EventGroupAdmin)
admin.site.register(Event,EventAdmin)