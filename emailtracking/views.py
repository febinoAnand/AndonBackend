from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .tasks import inboxReadTask
from rest_framework import viewsets
from .models import Inbox , Parameter, Setting, Trigger, ParameterFilter, Ticket
from .serializers import InboxSerializer, ParameterSerializer, SettingSerializer, TriggerSerializer, ParameterFilterSerializer, TicketSerializer

# Create your views here.

def readMailView(request):
    inboxReadTask.delay("Read from views")
    return HttpResponse("Task Called..")

class InboxViewSet(viewsets.ModelViewSet):
    queryset = Inbox.objects.all()
    serializer_class = InboxSerializer


class ParameterViewSet(viewsets.ModelViewSet):
    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer


class SettingViewSet(viewsets.ModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer

class TriggerViewSet(viewsets.ModelViewSet):
    queryset = Trigger.objects.all()
    serializer_class = TriggerSerializer

class ParameterFilterViewSet(viewsets.ModelViewSet):
    queryset = ParameterFilter.objects.all()
    serializer_class = ParameterFilterSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer