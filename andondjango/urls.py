"""
URL configuration for andondjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from django.contrib.staticfiles.urls import staticfiles_urlpatterns



urlpatterns = [
    path('admin/', admin.site.urls),
    path('config/', include('configuration.urls')),
    path('data/', include('data.urls')),
    path('devices/', include('devices.urls')),
    path('events/', include('events.urls')),
    path('smsgateway/', include('smsgateway.urls')),

    path('', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}

    ), name='AndonAPI'),

    path('openapi', get_schema_view(
        title="Andon Project",
        description="API for Andon events and config",
        version="1.0.0"
    ), name='openapi-schema'),

]

urlpatterns += staticfiles_urlpatterns()

