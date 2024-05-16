from django.urls import path,include
from .views import *
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register('unauthuser',UnauthUserViewSet)
router.register('userdetail',UserDetailViewSet)
router.register('setting',SettingViewSet)


urlpatterns =[
    path('',include(router.urls)),
    path("userauth/",UserAuthAPI.as_view()),
    path("userprompt/",UserAuthPrompt.as_view()),
    path("userverify/",UserVerifyView.as_view()),
    path("userregister/",UserRegisterView.as_view()),
    path("resendotp/",ResendOTPView.as_view()),
    path("userauthtoken/",obtain_auth_token)
]
