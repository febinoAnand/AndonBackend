from django.urls import path,include
from .views import *
from rest_framework import routers


router = routers.DefaultRouter()
router.register('unauthuser',UnauthUserViewSet)
router.register('userdetail',UserDetailViewSet)
router.register('setting',SettingViewSet)
from django.urls import path
from . import views


    

urlpatterns =[
    path('',include(router.urls)),
    path('receive-data/', views.receive_api_data, name='receive_data'),

    
]


    