from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from .views import *
from .views import GroupViewSet

router = routers.DefaultRouter()
router.register('unauthuser', UnauthUserViewSet)
router.register('userdetail', UserDetailViewSet)
router.register('setting', SettingViewSet)
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
    path('userchangepassword/', ChangePasswordView.as_view(), name='change-password'),
    path('userlogin/', LoginView.as_view(), name='login'),
    path('userlogout/', LogoutView.as_view(), name='logout'),
    path('delete-user/<int:user_id>/', DeleteUserView.as_view(), name='delete-user'),
    path('weblogin/', WebLoginView.as_view(), name='weblogin'),
    path('weblogout/', WebLogoutView.as_view(), name='weblogout')
]




