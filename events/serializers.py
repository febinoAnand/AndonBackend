from rest_framework import serializers

from devices.serializers import MachineSerializer
from .models import *

class ButtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Button
        fields = ('id','buttonID','buttonName','buttonColorName','buttonColor','buttonDO','buttonMode')

class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        fields = ('id','indicatorID','indicatorpin','indicatorColor','indicatorColorName')

class ProblemCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemCode
        fields = ('id','problemCode','problemName','problemDescription','problemType')

class EventSerializer(serializers.ModelSerializer):
    button = ButtonSerializer()
    problem = ProblemCodeSerializer()
    indicator = IndicatorSerializer()
    # deviceToken = serializers.CharField()
    class Meta:
        model = Event
        fields = ('id','eventID','button','problem','indicator','acknowledgeUser','notifyUser')

class EventShortSerializer(serializers.ModelSerializer):
    button = ButtonSerializer()
    indicator = IndicatorSerializer()

    class Meta:
        model = Event
        fields = ('id','eventID','button','indicator','acknowledgeUser','notifyUser')



class EventGroupSerializer(serializers.ModelSerializer):
    events = EventSerializer(many=True)
    machines = MachineSerializer(many=True)
    class Meta:
        model = EventGroup
        fields = ('id','groupID','groupName','events','machines')

class EventGroupsSerializerShort(serializers.ModelSerializer):
    events = EventShortSerializer(many=True)
    class Meta:
        model = EventGroup
        fields = ('id','groupID','groupName','events')

class MachineEventsGroupSerializer(serializers.ModelSerializer):
    processList = EventGroupsSerializerShort(source='machinesList',many=True)
    class Meta:
        model = Machine
        fields = ('machineID','name','model','processList')