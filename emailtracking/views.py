from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .tasks import inboxReadTask
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import get_user_model


# Create your views here.

def readMailView(request):
    inboxReadTask.delay("Read from views")
    return HttpResponse("Task Called..")

class InboxViewSet(viewsets.ModelViewSet):
    queryset = Inbox.objects.all()
    serializer_class = InboxSerializer
    http_method_names = ['get','delete']
    permission_classes = [IsAuthenticated]


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    http_method_names = ['get','delete']
    permission_classes = [IsAuthenticated]


class EmailIDViewSet(viewsets.ModelViewSet):
    queryset = EmailID.objects.all()
    serializer_class = EmailIDSerializer
    permission_classes = [IsAuthenticated]


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    http_method_names = ['get','delete']
    permission_classes = [IsAuthenticated]


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]


class SettingViewSet(viewsets.ModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer
    permission_classes = [IsAuthenticated]


class DashboardStatistics(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        User = get_user_model()
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        inactive_users = total_users - active_users
        total_departments = Department.objects.count()
        total_inbox = Inbox.objects.count()
        total_tickets = Ticket.objects.count()

        data = {
            'total_users': total_users,
            'active_users': active_users,
            'inactive_users': inactive_users,
            'total_departments': total_departments,
            'total_inbox': total_inbox,
            'total_tickets': total_tickets,
        }

        serializer = DashboardSerializer(data)
        return Response(serializer.data)
