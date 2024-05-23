from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('inbox',InboxViewSet)
router.register('parameter',ParameterViewSet, basename="parameter")
router.register('setting',SettingViewSet, basename="setting")
router.register('trigger',TriggerViewSet, basename="trigger")
router.register('filter',ParameterFilterViewSet, basename="filter")
router.register('ticket',TicketViewSet, basename="ticket")

urlpatterns =[
    path('readmail/',readMailView),
    path('',include(router.urls)),
]

