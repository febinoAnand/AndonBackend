from rest_framework import serializers
from .models import MQTT,UART

class MQTTSerializer(serializers.ModelSerializer):
    class Meta:
        model = MQTT
        fields = '__all__'

class UARTSerializer(serializers.ModelSerializer):
    class Meta:
        model = UART
        fields = '__all__'