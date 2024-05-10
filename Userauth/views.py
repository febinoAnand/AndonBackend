from django.shortcuts import render
from rest_framework import viewsets
from .models import UnauthUser, UserDetail, Setting
from .serializers import UnauthUserSerializer, UserDetailSerializer, SettingSerializer

# Create your views here.

class UnauthUserViewSet(viewsets.ModelViewSet):
    serializer_class = UnauthUserSerializer
    queryset = UnauthUser.objects.all().order_by('-pk')

class UserDetailViewSet(viewsets.ModelViewSet):
    serializer_class = UserDetailSerializer
    queryset = UserDetail.objects.all().order_by('-pk')

class SettingViewSet(viewsets.ModelViewSet):
    serializer_class = SettingSerializer
    queryset = Setting.objects.all().order_by('-pk')