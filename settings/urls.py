from django.urls import path
from .views import SettingListCreateView

urlpatterns = [
    path('', SettingListCreateView.as_view(), name='setting-list-create'),
]
