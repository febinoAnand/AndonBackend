from rest_framework import serializers
from .models import *

class SendReportViewSerializer(serializers.ModelSerializer):
    users_group  = serializers.SlugRelatedField(slug_field='name', queryset=Group.objects.all())
    send_to_user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta :
        model = SendReport
        fields = ('__all__')

class NotificationAuthViewSerializer(serializers.ModelSerializer):
    class Meta :
        model = NotificationAuth
        fields = ('__all__' )

class SettingViewSerializer(serializers.ModelSerializer):
    class Meta :
        model = Setting
        fields = ('__all__')