from rest_framework import generics, status
from rest_framework.response import Response
from django.http import Http404
from .models import Inbox, Settings
from .serializers import InboxSerializer, SettingsSerializer

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