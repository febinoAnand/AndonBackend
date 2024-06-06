from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class InboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inbox
        fields = ("__all__")

class TicketSerializer(serializers.ModelSerializer):
    inboxMessage = serializers.SlugRelatedField(slug_field='message', queryset=Inbox.objects.all())
    class Meta:
        model = Ticket
        fields = ("__all__")



class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username"]

class GroupUserSerializer(serializers.ModelSerializer):
    user_list = serializers.SerializerMethodField()
    def get_user_list(self,obj):
        users = User.objects.filter(groups__name = obj.name)
        userSer = UserSerializer(users,many=True)
        return userSer.data
    
    class Meta:
        model = Group
        fields = ["id","name","user_list"]

class ParameterSerializer(serializers.ModelSerializer):
    group_details = GroupUserSerializer(source='groups', many=True, read_only=True)
    
    class Meta:
        model = Parameter
        fields = "__all__"

class ShortParameterSerializer(serializers.ModelSerializer):
    group_details = GroupUserSerializer(source='groups', many=True, read_only=True)
    # user_list = serializers.SerializerMethodField()

    def get_user_list(self,obj):
        users = User.objects.filter(groups__name = obj.groups.name)
        userSer = UserSerializer(users,many=True)
        return userSer.data

    # fields1 = serializers.SerializerMethodField()
    class Meta:
        model = Parameter
        fields = ['field',"color","group_details"]
        

class ParameterFilterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ParameterFilter
        fields = "__all__"

    def to_internal_value(self, data):
        if isinstance(data, int):
            parameter_filter_instance = ParameterFilter.objects.get(pk=data)
            return {'operator': parameter_filter_instance.operator, 'value': parameter_filter_instance.value}
        return super().to_internal_value(data)
    
class ShortParameterFilterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ParameterFilter
        fields = ("id","operator","value","logical_operator")

class TriggerSerializer(serializers.ModelSerializer):
    group_to_send = serializers.SlugRelatedField(slug_field='name', queryset=Group.objects.all())
    # trigger_field = ParameterSerializer()
    
    trigger_field_details = ShortParameterSerializer(source="trigger_field",read_only=True)
    trigger_field = serializers.SlugRelatedField(slug_field='alias', queryset=Parameter.objects.all())
    
    # parameter_filter_list = serializers.SlugRelatedField(slug_field='name', queryset=Group.objects.all())
    # parameter_filter_list = serializers.SerializerMethodField()
    parameter_filter_list_details = ParameterFilterSerializer(read_only=True,source="parameter_filter_list",many=True)

    


    # def get_parameter_filter_list(self,obj):
    #     param = ParameterFilter.objects.filter(trigger_fields = obj)
    #     paramSer = ShortParameterFilterSerializer(param,many=True)
    #     return paramSer.data
    
    
    class Meta:
        model = Trigger
        fields = ("__all__")

class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ("__all__")

class ShortTriggerSerializer(serializers.ModelSerializer):
    rules = serializers.SerializerMethodField()

    def get_rules(self,obj):
        param = ParameterFilter.objects.filter(trigger_fields = obj)
        paramSer = ShortParameterFilterSerializer(param,many=True)
        return paramSer.data
    
    class Meta:
        model = Trigger
        fields = ("trigger_name","notification_message","users_to_send","rules")

class ShortTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("ticketname","required_json",)


class ReportSerializer(serializers.ModelSerializer):
    active_trigger = ShortTriggerSerializer()
    ticket = ShortTicketSerializer()
    class Meta:
        model = Report
        fields = ("__all__")