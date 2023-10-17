from rest_framework import serializers
from .models import *

class ButtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Button
        fields = ('id','buttonID','buttonName','buttonColorName','buttonColor')

class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        fields = ('id','indicatorID','indicatorpin','indicatorColor','indicatorColorName')

class ProblemCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemCode
        fields = ('id','problemCode','problemName','problemDescription')

class EventSerializer(serializers.ModelSerializer):
    button = ButtonSerializer()
    problem = ProblemCodeSerializer()
    indicator = IndicatorSerializer()
    # deviceToken = serializers.CharField()
    class Meta:
        model = Event
        fields = ('id','eventID','button','problem','indicator','acknowledgeUser','notifyUser')

class EventGroupSerializer(serializers.ModelSerializer):
    events = EventSerializer(many=True)
    # deviceToken = serializers.CharField()
    class Meta:
        model = EventGroup
        fields = ('id','groupID','events')
        # fields = ('groupID','eventsSerial')