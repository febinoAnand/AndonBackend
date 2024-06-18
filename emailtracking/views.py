from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .tasks import inboxReadTask
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *

# Create your views here.

@login_required
def readMailView(request):
    inboxReadTask.delay("Read from views")
    return HttpResponse("Task Called..")

class InboxViewSet(viewsets.ModelViewSet):
    queryset = Inbox.objects.all()
    serializer_class = InboxSerializer
    http_method_names = ['get', 'delete']
    permission_classes = [IsAuthenticated]

class ParameterViewSet(viewsets.ModelViewSet):
    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer
    permission_classes = [IsAuthenticated]

class SettingViewSet(viewsets.ModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer
    http_method_names = ["get", "post", "put"]
    permission_classes = [IsAuthenticated]

class TriggerViewSet(viewsets.ModelViewSet):
    queryset = Trigger.objects.all()
    serializer_class = TriggerSerializer
    permission_classes = [IsAuthenticated]

class ParameterFilterViewSet(viewsets.ModelViewSet):
    queryset = ParameterFilter.objects.all()
    serializer_class = ParameterFilterSerializer
    permission_classes = [IsAuthenticated]

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    http_method_names = ["get"]
    permission_classes = [IsAuthenticated]

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    http_method_names = ["get"]
    permission_classes = [IsAuthenticated]

class EmailIDViewSet(viewsets.ModelViewSet):
    queryset = EmailID.objects.all()
    serializer_class = EmailIDSerializer
    permission_classes = [IsAuthenticated]
