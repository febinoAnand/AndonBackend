from django.urls import path,include
from rest_framework import routers
from .views import MachineViewSet, DeviceViewSet, RFIDViewSet, UnRegisteredViewSet, DeviceVerification, TokenAuthentication, UnRegisterViewSetPostMethod



router = routers.DefaultRouter()
router.register('machine',MachineViewSet)
router.register('device',DeviceViewSet)
# router.register('rfid',RFIDViewSet)
router.register('unregister', UnRegisteredViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('verify/', DeviceVerification.as_view()),
    path('getToken/', TokenAuthentication.as_view()),
    path('register/', UnRegisterViewSetPostMethod.as_view()),


]
