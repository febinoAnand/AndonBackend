from django.urls import path, include
from .views import \
    SendReportViewSet, \
    SettingViewSet \

from rest_framework import routers


router = routers.DefaultRouter()
router.register('sendreport',SendReportViewSet)
router.register('setting',SettingViewSet)

urlpatterns = [
    path('',include(router.urls)),
]