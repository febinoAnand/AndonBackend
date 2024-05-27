from rest_framework import serializers
from .models import *

from django.contrib.auth.models import User

class UnauthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnauthUser
        fields = ('mobile_no','createdatetime','otp','emailaddress','session_id','device_id','otp_called','designation','is_existing_user','verification_token')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email','first_name',"last_name")
        # read_only_fields = ('username','email','first_name',"last_name")

class UserDetailSerializer(serializers.ModelSerializer):
    usermod = UserSerializer(source="extUser",read_only=True)
    userdetail_id = serializers.IntegerField(source = "id")
    user_id = serializers.IntegerField(source = "extUser.id")
    userActive = serializers.BooleanField(source="extUser.is_active")
    class Meta:
        model = UserDetail
        fields = ('userdetail_id','user_id','usermod','designation','mobile_no','device_id','auth_state','expiry_time',"userActive")


class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ('all_user_expiry_time','OTP_resend_interval','OTP_valid_time','OTP_call_count','OTP_wrong_count')


        
class UserAuthAPISerializer(serializers.Serializer):
    appToken = serializers.UUIDField(required=True,allow_null=False)
    mobileno = serializers.CharField(required=True,max_length=15,allow_null=False)
    email = serializers.EmailField(required=True,allow_null=False)
    deviceID = serializers.UUIDField(required=True,allow_null=False)



class UserAuthPromptSerializer(serializers.Serializer):
    appToken = serializers.UUIDField(required=True,allow_null=False)
    sessionID = serializers.UUIDField(required=True,allow_null=False)
    deviceID = serializers.UUIDField(required=True,allow_null=False)
    needtochange = serializers.BooleanField(allow_null=False)
    # isExistingUser = serializers.BooleanField(allow_null=False)


class UserAuthVerifySerializer(serializers.Serializer):
    appToken = serializers.UUIDField(required=True,allow_null=False)
    sessionID = serializers.UUIDField(required=True,allow_null=False)
    OTP = serializers.DecimalField(required=True,max_digits=5,decimal_places=0,allow_null=False)
    deviceID = serializers.UUIDField(required=True,allow_null=False)



class UserAuthRegisterSerializer(serializers.Serializer):
    appToken = serializers.UUIDField(required=True,allow_null=False)
    sessionID = serializers.UUIDField(required=True,allow_null=False)
    deviceID = serializers.UUIDField(required=True,allow_null=False)
    designation = serializers.CharField(max_length=15, required=True,allow_null=False)
    name = serializers.CharField(max_length=30, required=True,allow_null=False)
    password = serializers.CharField(max_length=30, required=True,allow_null=False)
    notificationID = serializers.CharField(max_length=50, required=True,allow_null=False)


