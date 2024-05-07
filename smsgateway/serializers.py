from rest_framework import serializers
from .models import *

class SendReportViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendReport
        fields = ("date","time","to_number","from_number","message","delivery_status")

class SettingViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ("sid","auth_token","number")