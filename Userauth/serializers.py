from rest_framework import serializers
from .models import *

class UnauthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnauthUser
        fields = ('mobile_no','createdatetime','otp','emailaddress','session_id','device_id','otp_called','designation','is_existing_user','verification_token')

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = ('extUser','designation','mobile_no','device_id','auth_state','expiry_time')

class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ('all_user_expiry_time','OTP_resend_interval','OTP_valid_time','OTP_call_count','OTP_wrong_count')


        
class UserAuthAPISerializer(serializers.Serializer):
    appToken = serializers.UUIDField(required=True,allow_null=False)
    mobileno = serializers.CharField(required=True,max_length=15,allow_null=False)
    email = serializers.EmailField(required=True,allow_null=False)
    deviceID = serializers.UUIDField(required=True,allow_null=False)