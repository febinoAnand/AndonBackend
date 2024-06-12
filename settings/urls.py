from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SettingViewSet

router = DefaultRouter()
router.register(r'settings', SettingViewSet, basename='setting')

urlpatterns = [
    path('', include(router.urls)),
]
