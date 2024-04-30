from rest_framework import serializers
from .models import Inbox, Settings, SearchParameter, UserEmailTracking

class InboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inbox
        fields = ('date','time','from_email','to_email','subject','message','message_id')

class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = ('host','port','username','password','checkstatus','checkinterval','phone','sid','auth_token')

class SearchParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchParameter
        fields = ('name','hunt_word','message','user_group')

    def to_representation(self, instance):
        rep = super(SearchParameterSerializer, self).to_representation(instance)
        rep['user_group'] = instance.user_group.name
        return rep

class UserEmailTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEmailTracking
        fields = ('user','designation','mobile')

    def to_representation(self, instance):
        rep = super(UserEmailTrackingSerializer, self).to_representation(instance)
        rep['user'] = instance.user.username
        return rep