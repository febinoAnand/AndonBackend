from rest_framework import serializers
from .models import *

class SendReportView(serializers.ModelSerializer):
    class meta :
        model = SendReport
        fields = ("date","time","title","message","send_to_user","users_group","delivery_status")

class NotificationAuthView(serializers.ModelSerializer):
    class meta :
        model = NotificationAuth
        fields = ("noti_token", "user_to_auth" )

class SettingView(serializers.ModelSerializer):
    class meta :
        model = Setting
        fields = ("application_id")