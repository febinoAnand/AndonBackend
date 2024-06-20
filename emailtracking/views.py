from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .tasks import inboxReadTask
from rest_framework import viewsets
from .models import *
from .serializers import *

# Create your views here.

def readMailView(request):
    inboxReadTask.delay("Read from views")
    return HttpResponse("Task Called..")

class InboxViewSet(viewsets.ModelViewSet):
    queryset = Inbox.objects.all()
    serializer_class = InboxSerializer
    http_method_names = ['get','delete']


# class ParameterViewSet(viewsets.ModelViewSet):
#     queryset = Parameter.objects.all()
#     serializer_class = ParameterSerializer


# class SettingViewSet(viewsets.ModelViewSet):
#     queryset = Setting.objects.all()
#     serializer_class = SettingSerializer
#     http_method_names = ["get","post","put"]

# class TriggerViewSet(viewsets.ModelViewSet):
#     queryset = Trigger.objects.all()
#     serializer_class = TriggerSerializer

# class ParameterFilterViewSet(viewsets.ModelViewSet):
#     queryset = ParameterFilter.objects.all()
#     serializer_class = ParameterFilterSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    http_method_names=["get"]

# class ReportViewSet(viewsets.ModelViewSet):
#     queryset = Report.objects.all()
#     serializer_class = ReportSerializer
#     http_method_names = ["get"]

class EmailIDViewSet(viewsets.ModelViewSet):
    queryset = EmailID.objects.all()
    serializer_class = EmailIDSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer