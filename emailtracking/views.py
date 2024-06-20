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


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    http_method_names = ['get','delete']


class EmailIDViewSet(viewsets.ModelViewSet):
    queryset = EmailID.objects.all()
    serializer_class = EmailIDSerializer


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    http_method_names = ['get','delete']

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer