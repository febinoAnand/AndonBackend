from django.urls import path,include
from .views import *
from rest_framework import routers


router = routers.DefaultRouter()
router.register('unauthuser',UnauthUserViewSet)
router.register('userdetail',UserDetailViewSet)
router.register('setting',SettingViewSet)

urlpatterns =[
    path('',include(router.urls)),
]
