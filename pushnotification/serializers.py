from rest_framework import serializers
from .models import *

class SendReportViewSerializer(serializers.ModelSerializer):
    class Meta :
        model = SendReport
        fields = ('date','time','title','message','send_to_user','users_group','delivery_status')

class NotificationAuthViewSerializer(serializers.ModelSerializer):
    class Meta :
        model = NotificationAuth
        fields = ('noti_token', 'user_to_auth' )

class SettingViewSerializer(serializers.ModelSerializer):
    class Meta :
        model = Setting
        fields = ('__all__')