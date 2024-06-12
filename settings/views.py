from rest_framework import viewsets
from settings.models import Setting
from settings.serializers import SettingSerializer
from rest_framework.exceptions import ValidationError

class SettingViewSet(viewsets.ModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer

    
