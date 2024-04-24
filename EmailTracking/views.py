from rest_framework import generics, status
from rest_framework.response import Response
from django.http import Http404
from .models import Inbox, Settings
from .serializers import InboxSerializer, SettingsSerializer

class InboxView(generics.ListCreateAPIView):
    queryset = Inbox.objects.all()
    serializer_class = InboxSerializer

    def delete(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            if not queryset.exists():
                raise Http404('No Inbox instances found.')
            instance = queryset.first()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404 as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)

class SettingsView(generics.RetrieveUpdateAPIView):
    serializer_class = SettingsSerializer

    def get_object(self):
        try:
            return Settings.objects.get(pk=1)
        except Settings.DoesNotExist:
            raise Http404("Settings does not exist")

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)