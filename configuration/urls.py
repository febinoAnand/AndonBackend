from django.urls import path,include
from rest_framework import routers
from .views import MQTTViewSet,UARTViewSet


router = routers.DefaultRouter()
# router.register('mqtt', MQTTViewSet)
# router.register('uart',UARTViewSet)

urlpatterns = [
    path('',include(router.urls))
]