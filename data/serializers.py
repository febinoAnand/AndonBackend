from rest_framework import serializers
from .models import RawData, ProblemData, LastProblemData
from events.serializers import *
from devices.serializers import *

class RawSerializer(serializers.ModelSerializer):
    # deviceToken = serializers.CharField()
    class Meta:
        model = RawData
        fields = ('date','time','eventID','deviceID','eventGroupID','data')

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