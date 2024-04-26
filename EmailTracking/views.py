from rest_framework import generics, status
from rest_framework.response import Response
from django.http import Http404
from .models import Inbox, Settings, SearchParameter
from .serializers import InboxSerializer, SettingsSerializer, SearchParameterSerializer
import logging
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)

class InboxView(generics.ListCreateAPIView):
    queryset = Inbox.objects.all()
    serializer_class = InboxSerializer
    http_method_names = ['get', 'delete']

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_queryset().first()
            if instance:
                instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
class SettingsView(generics.RetrieveUpdateAPIView):
    serializer_class = SettingsSerializer
    allowed_methods = ['GET', 'PUT']

    def get_object(self):
        try:
            return Settings.objects.first()
        except Settings.DoesNotExist:
            raise Http404("Settings does not exist")

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data) 

class SearchParameterAPIView(generics.GenericAPIView):
    queryset = SearchParameter.objects.all()
    serializer_class = SearchParameterSerializer

    def get(self, request, *args, **kwargs):
        search_parameters = self.get_queryset()
        serializer = self.get_serializer(search_parameters, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        hunt_word = request.data.get('hunt_word')
        if hunt_word:
            try:
                instance = SearchParameter.objects.get(hunt_word=hunt_word)
            except SearchParameter.DoesNotExist:
                return Response({'error': 'SearchParameter not found.'}, status=status.HTTP_404_NOT_FOUND)

            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({'error': 'Please provide hunt_word in request body.'}, status=status.HTTP_400_BAD_REQUEST)