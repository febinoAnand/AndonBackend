from django.shortcuts import render
from rest_framework import viewsets
from .models import Inbox, Ticket, Parameter, ParameterFilter, Trigger, Setting
from .serializers import InboxViewSerializer, TicketViewSerializer, ParameterViewSerializer, ParameterFilterViewSerializer, TriggerViewSerializer, SettingViewSerializer

# Create your views here.


class InboxViewSet(viewsets.ModelViewSet):
    serializer_class = InboxViewSerializer
    queryset = Inbox.objects.all().order_by('-pk')

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketViewSerializer
    queryset = Ticket.objects.all().order_by('-pk')

class ParameterViewSet(viewsets.ModelViewSet):
    serializer_class = ParameterViewSerializer
    queryset = Parameter.objects.all().order_by('-pk')

class ParameterFilterViewSet(viewsets.ModelViewSet):
    serializer_class = ParameterFilterViewSerializer
    queryset = ParameterFilter.objects.all().order_by('-pk')

class TriggerViewSet(viewsets.ModelViewSet):
    serializer_class = TriggerViewSerializer
    queryset = Trigger.objects.all().order_by('-pk')

class SettingViewSet(viewsets.ModelViewSet):
    serializer_class = SettingViewSerializer
    queryset = Setting.objects.all().order_by('-pk')