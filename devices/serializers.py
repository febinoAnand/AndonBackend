from rest_framework import serializers
from .models import *



class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('id','deviceID','model','hardwareVersion','softwareVersion')


class MachineSerializer(serializers.ModelSerializer):
    device = DeviceSerializer()
    class Meta:
        model = Machine
        fields = ('id','machineID','name','manufacture','model','line','device')


class MachineWithoutDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ('id','machineID','name','manufacture','model','line')
    # def create(self, validated_data):
    #     print("trying to create")
    #     print(validated_data)
    #     return {"message":"ok"}
    #
    #
    # def update(self, instance, validated_data):
    #     print ("tryin to update")



class RFIDSerializer(serializers.ModelSerializer):
    rfidUser = serializers.SerializerMethodField();

    def get_rfidUser(self,obj):
        return obj.rfidUser.username

    class Meta:
        model = RFID
        fields = ('rfid','rfidUser')

class UnRegisteredSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnRegisteredDevice
        fields = ('sessionID','deviceID','devicePassword','model','hardwareVersion','softwareVersion','OTP')

class UnRegisteredGetMethodSerializer(serializers.Serializer):
    deviceID = serializers.CharField()
    model = serializers.CharField()
    hardwareVersion = serializers.CharField()
    softwareVersion = serializers.CharField()
    devicePassword = serializers.CharField()
    class Meta:
        fields = ('deviceID','devicePassword','model','hardwareVersion','softwareVersion')


class VerifyDeviceSerializer(serializers.Serializer):
    sessionID = serializers.UUIDField()
    OTP = serializers.CharField()
    # class Meta:
    #     fields = ('OTP','sessionID')

class GetTokenSerializer(serializers.Serializer):
    deviceID = serializers.CharField()
    devicePassword = serializers.CharField()

