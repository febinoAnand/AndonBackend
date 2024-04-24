from django.contrib import admin
from .models import Settings, Inbox

# Register your models here.

admin.site.register(Inbox)
admin.site.register(Settings)