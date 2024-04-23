from django.contrib import admin
from .models import UART, MQTT, Port

# Register your models here.
# admin.site.register(UART)
# admin.site.register(MQTT)
admin.site.register(Port)

@admin.register(MQTT)
class MQTTModelAdmin(admin.ModelAdmin):
    list_display = ['host','port','username','password']
    def has_add_permission(self, request):
        # if there's already an entry, do not allow adding
        count = MQTT.objects.all().count()
        if count == 0:
            return True
        return False

@admin.register(UART)
class UARTModelAdmin(admin.ModelAdmin):
    list_display = ["comport","baudrate",'parity','databit','stopbit']
    def has_add_permission(self, request):
        count = UART.objects.all().count()
        if count == 0:
            return True
        return False