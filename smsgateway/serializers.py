from rest_framework import serializers
from .models import *

class SendReportViewSerializer(serializers.ModelSerializer):
    from_number = serializers.CharField(source='from_number.smsnumber')

    class Meta:
        model = SendReport
        fields = ("date", "time", "to_number", "from_number", "message", "delivery_status")

class SettingViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ('__all__')