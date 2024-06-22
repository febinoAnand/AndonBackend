from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework.exceptions import MethodNotAllowed
from django.utils.timezone import now, timedelta
from django.db.models import Q
from Userauth.models import UserDetail 

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


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = ['designation', 'mobile_no', 'device_id', 'auth_state', 'expiry_time']

class UserSerializer(serializers.ModelSerializer):
    user_detail = UserDetailSerializer(source='userdetail', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'user_detail']


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
        fields = ['id','date','time','ticketname', 'inboxMessage', 'actual_json', 'is_satisfied']
    
   
class ReportSerializer(serializers.ModelSerializer):
    send_to_user = UserSerializer(many=True)
    class Meta:
        model = Report
        fields = '__all__'
    

class DepartmentSerializer(serializers.ModelSerializer):
        class Meta:
            model = Department
            fields = '__all__'

class DashboardSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    active_users = serializers.IntegerField()
    inactive_users = serializers.IntegerField()
    total_departments = serializers.IntegerField()
    total_inbox = serializers.IntegerField()
    total_tickets = serializers.IntegerField()
    department_ticket_count = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    def get_department_ticket_count(self, obj):
        last_24_hours = now() - timedelta(hours=24)
        last_24_date = last_24_hours.date()
        last_24_time = last_24_hours.time()

        departments = Department.objects.all()
        department_ticket_count = []

        for department in departments:
            try:
                ticket_count = Report.objects.filter(
                    Department=department.dep_alias
                ).filter(
                    Q(date__gt=last_24_date) | (Q(date=last_24_date) & Q(time__gte=last_24_time))
                ).count()
            except Exception as e:
                ticket_count = 0
            department_ticket_count.append({
                'department_id': department.id,
                'department_name': department.dep_alias,
                'ticket_count': ticket_count
            })

        return department_ticket_count
    
    def get_user_details(self, obj):
        users = User.objects.all()
        return UserSerializer(users, many=True).data
