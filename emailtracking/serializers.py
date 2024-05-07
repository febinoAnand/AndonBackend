from rest_framework import serializers
from .models import *

class InboxViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inbox
        fields = ("date","time","from_email","to_email","subject","message","message_id")

class TicketViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("ticketname","date","time","inboxMessage","actual_json","required_json","log")

class ParameterViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ("alias","field","datatype")

class ParameterFilterViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParameterFilter
        fields = ("operator","value")

class TriggerViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trigger
        fields = ("__all__")

class SettingViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ("host","port","username","password","checkstatus","checkinterval","phone","sid","auth_token")