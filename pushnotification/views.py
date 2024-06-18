from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import SendReport, NotificationAuth, Setting
from .serializers import SendReportViewSerializer, NotificationAuthViewSerializer, SettingViewSerializer

# Create your views here.

class SendReportViewSet(viewsets.ModelViewSet):
    serializer_class = SendReportViewSerializer
    queryset = SendReport.objects.all()
    permission_classes = [IsAuthenticated]

class NotificationAuthViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationAuthViewSerializer
    queryset = NotificationAuth.objects.all()
    permission_classes = [IsAuthenticated]

class SettingViewSet(viewsets.ModelViewSet):
    serializer_class = SettingViewSerializer
    queryset = Setting.objects.all()
    permission_classes = [IsAuthenticated]
