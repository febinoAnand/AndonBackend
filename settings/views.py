from rest_framework import generics
from settings.models import Setting
from settings.serializers import SettingSerializer

class SettingListCreateView(generics.ListCreateAPIView):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer

