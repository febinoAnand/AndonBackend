from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from .views import *


router = routers.DefaultRouter()
router.register('unauthuser', UnauthUserViewSet)
router.register('userdetail', UserDetailViewSet)
router.register('setting', SettingViewSet)

from django.urls import path, include
from rest_framework import routers
from .views import GroupViewSet

router = routers.DefaultRouter()
router.register('groups', GroupViewSet, basename="group")

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
    path('groups/<int:id>/add-users/', GroupUserAddView.as_view(), name='group-add-users'),
    path('groups/<int:id>/remove-users/', GroupUserRemoveView.as_view(), name='group-remove-users'),
]




