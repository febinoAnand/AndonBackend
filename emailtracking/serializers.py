from rest_framework import serializers
from .models import *

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

class ParameterSerializer(serializers.ModelSerializer):
    group_details = GroupSerializer(source='groups', many=True, read_only=True)

    class Meta:
        model = Parameter
        fields = "__all__"



class ParameterFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParameterFilter
        fields = "__all__"

    def to_internal_value(self, data):
        if isinstance(data, int):
            parameter_filter_instance = ParameterFilter.objects.get(pk=data)
            return {'operator': parameter_filter_instance.operator, 'value': parameter_filter_instance.value}
        return super().to_internal_value(data)

class TriggerSerializer(serializers.ModelSerializer):
    group_to_send = serializers.SlugRelatedField(slug_field='name', queryset=Group.objects.all())
    trigger_field = serializers.SlugRelatedField(slug_field='alias', queryset=Parameter.objects.all())
    parameter_filter_list = ParameterFilterSerializer(many=True, read_only=True)
    
    class Meta:
        model = Trigger
        fields = ("__all__")

class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ("__all__")