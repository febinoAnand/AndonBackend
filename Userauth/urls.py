from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from .views import *
from .views import GroupUsersAPIView
from .views import GroupListView

router = routers.DefaultRouter()
router.register('unauthuser', UnauthUserViewSet)
router.register('userdetail', UserDetailViewSet)
router.register('setting', SettingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('userauth/', UserAuthAPI.as_view()),
    path('userprompt/', UserAuthPrompt.as_view()),
    path('userverify/', UserVerifyView.as_view()),
    path('userregister/', UserRegisterView.as_view()),
    path('resendotp/', ResendOTPView.as_view()),
    path('userauthtoken/', obtain_auth_token, name='userauthtoken'),
    path('revoke-token/', RevokeAuthToken.as_view(), name='revoke_token'),
    path('groups/<int:group_id>/users/', GroupUsersAPIView.as_view(), name='group_users'),
    path('groups/', GroupListView.as_view(), name='group-list'),
]




