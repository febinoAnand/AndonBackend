from django.urls import path
from . import views

urlpatterns = [
    path('inbox', views.InboxView.as_view(), name='inbox-list'),
    path('settings', views.SettingsView.as_view(), name='settings-detail'),
    path('searchparameters', views.SearchParameterAPIView.as_view(), name='search-parameter'),
]
