from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework.exceptions import MethodNotAllowed

class InboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inbox
        fields = ("__all__")

class TicketSerializer(serializers.ModelSerializer):
    inboxMessage = serializers.PrimaryKeyRelatedField(queryset=Inbox.objects.all())
    
    class Meta:
        model = Ticket
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username","email"]

class GroupUserSerializer(serializers.ModelSerializer):
    user_list = serializers.SerializerMethodField()
    def get_user_list(self,obj):
        users = User.objects.filter(groups__name = obj.name)
        userSer = UserSerializer(users,many=True)
        return userSer.data
    
    class Meta:
        model = Group
        fields = ["id","name","user_list"]



class EmailIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailID
        fields = ['id', 'email', 'active']

class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = "__all__"

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'ticketname', 'inboxMessage', 'actual_json', 'is_satisfied']
    
   
class ReportSerializer(serializers.ModelSerializer):
    send_to_user = UserSerializer(many=True)
    class Meta:
        model = Report
        fields = '__all__'
    

class DepartmentSerializer(serializers.ModelSerializer):
        class Meta:
            model = Department
            fields = '__all__'
            