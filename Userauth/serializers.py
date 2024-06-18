from rest_framework import serializers
from .models import *
from django.contrib.auth.models import Group
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
    usermod = UserSerializer(source="extUser", read_only=True)
    userdetail_id = serializers.IntegerField(source="id")
    user_id = serializers.IntegerField(source="extUser.id", read_only=True)
    userActive = serializers.BooleanField(source="extUser.is_active")

    class Meta:
        model = UserDetail
        fields = ('userdetail_id', 'user_id', 'usermod', 'designation', 'mobile_no', 'device_id', 'auth_state', 'expiry_time', 'userActive')
    
    def update(self, instance, validated_data):
        ext_user_data = validated_data.pop('extUser', None)
        if ext_user_data and 'is_active' in ext_user_data:
            instance.extUser.is_active = ext_user_data['is_active']
            instance.extUser.save()

       
        return super().update(instance, validated_data)  


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


class UserAuthResendSerializer(serializers.Serializer):
    appToken = serializers.UUIDField(required=True,allow_null=False)
    sessionID = serializers.UUIDField(required=True,allow_null=False)
    deviceID = serializers.UUIDField(required=True,allow_null=False)



class UserSerializer(serializers.ModelSerializer):
    mobile_no = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'mobile_no']

    def get_mobile_no(self, obj):
        try:
            return obj.userdetail.mobile_no
        except UserDetail.DoesNotExist:
            return None

class AuthGroupSerializer(serializers.ModelSerializer):
    user_set = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'name', 'user_set', 'user_details']

    def get_user_details(self, obj):
        users = obj.user_set.all()
        user_serializer = UserSerializer(users, many=True)
        return user_serializer.data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user_details'] = self.get_user_details(instance)
        return representation


class LoginSerializer(serializers.Serializer):
    app_token = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    device_id = serializers.CharField(required=True)
    notification_id = serializers.CharField(required=True)

class LogoutSerializer(serializers.Serializer):
    app_token = serializers.CharField()
    device_id = serializers.CharField()

  


class ChangePasswordSerializer(serializers.Serializer):
    app_token = serializers.CharField(required=True)
    device_id = serializers.CharField(required=True)
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("New password and confirm password do not match.")
        return data





class WebLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class WebLogoutSerializer(serializers.Serializer):
    token = serializers.CharField()