from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

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
        fields = ["id","username"]

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
    class Meta:
        model = Report
        fields = '__all__'
        extra_kwargs = {
            'date': {'read_only': True},
            'time': {'read_only': True}
        }

    def update(self, instance, validated_data):
       
        date = validated_data.pop('date', None)
        time = validated_data.pop('time', None)
        
        
        instance = super().update(instance, validated_data)

        if date is not None:
            instance.date = date
        if time is not None:
            instance.time = time

 
        instance.save()
        
        return instance
    
class DepartmentSerializer(serializers.ModelSerializer):
        class Meta:
            model = Department
            fields = '__all__'
            read_only_fields = ('date', 'time')

        def update(self, instance, validated_data):
            
            validated_data.pop('date', None)
            validated_data.pop('time', None)
            
            
            instance = super().update(instance, validated_data)

           
            instance.time = timezone.now()
            
           
            instance.save()
            
            return instance