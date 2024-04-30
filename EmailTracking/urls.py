from django.urls import path
from . import views

urlpatterns = [
    path('inbox', views.InboxView.as_view(), name='inbox-list'),
    path('settings', views.SettingsView.as_view(), name='settings-detail'),
    path('searchparameters', views.SearchParameterAPIView.as_view(), name='search-parameter'),
    path('useremailtracking', views.UserEmailTrackingAPIView.as_view(), name='UserEmail_Tracking'),
    path('groupemailtracking', views.GroupEmailTrackingAPIView.as_view(), name='GroupEmail_Tracking'),
]
