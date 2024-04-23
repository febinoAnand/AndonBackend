from rest_framework import serializers
from .models import RawData, ProblemData, LastProblemData
from events.serializers import *
from devices.serializers import *

class RawSerializer(serializers.ModelSerializer):
    # deviceToken = serializers.CharField()
    class Meta:
        model = RawData
        fields = ('date','time','eventID','machineID','eventGroupID')

class RawSerializerWithDateTime(serializers.ModelSerializer):
    # deviceToken = serializers.CharField()
    class Meta:
        model = RawData
        fields = ('datetime','date','time','eventID','machineID','eventGroupID')

    # def to_representation(self, instance):
    #     data = super(RawSerializer, self).to_representation(instance)
    #     data.fields.datetime = data.fields.datetime.strftime("%Y-%m-%d %H:%M:%S")
    #     return data

class ProblemDataSerializer(serializers.ModelSerializer):
    eventGroupID = serializers.SerializerMethodField()
    event = EventSerializer(source='eventID',read_only=True)
    machine = MachineSerializer(source='machineID',read_only=True)

    def get_eventGroupID(self,obj):
        return obj.eventGroupID.groupID

    class Meta:
        model = ProblemData
        fields = ('date','time','eventGroupID','event','machine','issueTime','acknowledgeTime','endTime','dateTimeNow')

class LastProblemDataSerializer(serializers.ModelSerializer):
    event = EventSerializer(source="eventID",read_only=True)
    machine = MachineSerializer(source="machineID",read_only=True)
    eventGroupID = serializers.SerializerMethodField()

    def get_eventGroupID(self,obj):
        return obj.eventGroupID.groupID
    class Meta:
        model = LastProblemData
        fields = ('date','time','eventGroupID','event','machine','issueTime','acknowledgeTime','endTime','dateTimeNow')

# class LiveDataSerializer(serializers.Serializer):
#     # machines = MachineSerializer(source="machineID",read_only=True,many=True)
#     machines = serializers.SerializerMethodField()
#     currentEvent = serializers.SerializerMethodField()
#     class Meta:
#         fields = ['machines','currentEvent']
#
#     def get_machiens(self,obj):
#         return MachineSerializer(obj.machine.all(),many=True).data
#
#     def get_currentEvent(self,obj):
#         return EventSerializer(obj.event.all(),many=True).data

# class rawGetMethodeSerializer(serializers.Serializer):
#     dateTime = serializers.DateTimeField()
#     data = serializers.CharField()