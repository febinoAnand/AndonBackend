from django.contrib import admin
from .models import Settings, Inbox, SearchParameter

# Register your models here.

admin.site.register(Inbox)
admin.site.register(Settings)
admin.site.register(SearchParameter)