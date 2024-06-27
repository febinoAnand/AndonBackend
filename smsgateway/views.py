from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import SendReport, Setting
from .serializers import SendReportViewSerializer, SettingViewSerializer
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes

# Create your views here.

class SendReportViewSet(viewsets.ModelViewSet):
    serializer_class = SendReportViewSerializer
    queryset = SendReport.objects.all()
    permission_classes = [IsAuthenticated]

class SettingViewSet(viewsets.ModelViewSet):
    serializer_class = SettingViewSerializer
    queryset = Setting.objects.all()
    permission_classes = [IsAuthenticated]

@login_required
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sendSMS(request):
    return HttpResponse("Message sent")
