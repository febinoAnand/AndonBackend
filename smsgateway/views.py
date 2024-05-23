from django.shortcuts import render
from rest_framework import viewsets
from .models import SendReport, Setting
from .serializers import SendReportViewSerializer, SettingViewSerializer
from django.http import HttpResponse

# Create your views here.

class SendReportViewSet(viewsets.ModelViewSet):
    serializer_class = SendReportViewSerializer
    queryset = SendReport.objects.all()

class SettingViewSet(viewsets.ModelViewSet):
    serializer_class = SettingViewSerializer
    queryset = Setting.objects.all()

def sendSMS(request):

    return HttpResponse("Message sent")