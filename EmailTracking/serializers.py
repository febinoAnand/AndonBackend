from rest_framework import serializers
from .models import Inbox, Settings, SearchParameter, UserEmailTracking, GroupEmailTracking

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
    
class GroupEmailTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupEmailTracking
        fields = ('user_group','user_list')

    def get_user_list(self, instance):
        user_list = instance.user_list.all()
        user_names = [user.username for user in user_list]
        return user_names

    def get_user_list_count(self, instance):
        return instance.user_list.count()

    def to_representation(self, instance):
        rep = super(GroupEmailTrackingSerializer, self).to_representation(instance)
        rep['user_group'] = instance.user_group.name
        rep['user_list'] = self.get_user_list(instance)
        rep['user_list_count'] = self.get_user_list_count(instance)
        return rep

class GroupEmailSerializer(serializers.ModelSerializer):
    user_group = serializers.CharField()
    user_list = serializers.CharField()
    class Meta:
        model = GroupEmailTracking
        fields = "__all__"