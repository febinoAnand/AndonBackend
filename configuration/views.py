from rest_framework import viewsets
from .serializers import MQTTSerializer, UARTSerializer
from .models import MQTT, UART
from django.shortcuts import render

# Create your views here.
class MQTTViewSet(viewsets.ModelViewSet):
    schema = None
    serializer_class = MQTTSerializer
    queryset = MQTT.objects.all()
    http_method_names = ['get']

class UARTViewSet(viewsets.ModelViewSet):
    schema = None
    serializer_class = UARTSerializer
    queryset = UART.objects.all()
    http_method_names = ['get']