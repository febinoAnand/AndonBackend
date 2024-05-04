from django.urls import path, include
from .views import \
    InboxViewSet, \
    TicketViewSet, \
    ParameterViewSet, \
    ParameterFilterViewSet,\
    TriggerViewSet,\
    SettingViewSet

from rest_framework import routers


router = routers.DefaultRouter()
router.register('inbox',InboxViewSet)
router.register('ticket',TicketViewSet)
router.register('parameter',ParameterViewSet)
router.register('parameterfilter',ParameterFilterViewSet)
router.register('trigger',TriggerViewSet)
router.register('setting',SettingViewSet)



urlpatterns = [
    path('',include(router.urls)),
]
