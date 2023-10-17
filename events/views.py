from rest_framework import viewsets,status
from .models import *
from .serializers import *
from .models import *
from devices.models import Token
from django.shortcuts import render
from rest_framework.response import Response

# Create your views here.
class ButtonViewSet(viewsets.ModelViewSet):
    serializer_class = ButtonSerializer
    queryset = Button.objects.all()
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):

        if not authenticateDevice(request):
            errorJson = {"status":"Authentication Error. Invalid Token"}
            return Response(errorJson,status=status.HTTP_201_CREATED)

        queryset = Button.objects.all()
        serializer = ButtonSerializer(queryset, many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)

class IndicatorViewSet(viewsets.ModelViewSet):
    serializer_class = IndicatorSerializer
    queryset = Indicator.objects.all()
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):

        if not authenticateDevice(request):
            errorJson = {"status":"Authentication Error. Invalid Token"}
            return Response(errorJson,status=status.HTTP_201_CREATED)

        queryset = Indicator.objects.all()
        serializer = IndicatorSerializer(queryset, many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)

class ProblemCodeViewSet(viewsets.ModelViewSet):
    serializer_class = ProblemCodeSerializer
    queryset = ProblemCode.objects.all()
    http_method_names = ['get']
    def list(self, request, *args, **kwargs):

        if not authenticateDevice(request):
            errorJson = {"status":"Authentication Error. Invalid Token"}
            return Response(errorJson,status=status.HTTP_201_CREATED)

        queryset = ProblemCode.objects.all()
        serializer = ProblemCodeSerializer(queryset, many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    http_method_names = ['get']

    def create(self, request, *args, **kwargs):
        res = request.data
        # if not authenticateDevice(res):
        #     errorJson = {"status":"Authentication Error"}
        #     return Response(errorJson,status=status.HTTP_201_CREATED)

        button = Button.objects.get(id=res['button']['id'])
        indicator = Indicator.objects.get(id=(res['indicator']['id']))
        problem = ProblemCode.objects.get(id=(res['problem']['id']))

        Event.objects.create(
            eventID = res['eventID'],
            button = button,
            indicator = indicator,
            problem = problem
        )
        return Response(res,status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        res = request.data
        # authenticateDevice(res)

        button = Button.objects.get(id=res['button']['id'])
        indicator = Indicator.objects.get(id=res['indicator']['id'])
        problem = ProblemCode.objects.get(id=res['problem']['id'])
        event = Event.objects.get(id=res['id'])

        event.eventID = res['eventID']
        event.button = button
        event.indicator = indicator
        event.problem = problem
        event.save()
        return Response(res,status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):

        if not authenticateDevice(request):
            errorJson = {"status":"Authentication Error. Invalid Token"}
            return Response(errorJson,status=status.HTTP_201_CREATED)

        queryset = Event.objects.all()
        serializer = EventSerializer(queryset, many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)


class EventGroupViewSet(viewsets.ModelViewSet):
    serializer_class = EventGroupSerializer
    queryset = EventGroup.objects.all()
    http_method_names = ['get']

    def create(self, request, *args, **kwargs):
        res = request.data
        authenticateDevice(res)

        eventGroup = EventGroup(groupID = res["groupID"])
        events = res["events"]
        eventGroup.save()
        for event in events:
            currentEvent = Event.objects.get(id=event['id'])
            eventGroup.events.add(currentEvent)
        eventGroup.save()
        return Response(res,status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        res = request.data
        print(res)
        authenticateDevice(res)

        eventGroup = EventGroup.objects.get(id=res['id'])
        events = res['events']
        eventGroup.groupID = res["groupID"]
        eventGroup.events.clear()
        for event in events:
            currentEvent = Event.objects.get(id=event["id"])
            eventGroup.events.add(currentEvent)
        eventGroup.save()
        return Response(res, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):

        if not authenticateDevice(request):
            errorJson = {"status":"Authentication Error. Invalid Token"}
            return Response(errorJson,status=status.HTTP_201_CREATED)

        queryset = EventGroup.objects.all()
        serializer = EventGroupSerializer(queryset, many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)

def authenticateDevice(data):
    currentToken = data.META.get("HTTP_DEVICEAUTHORIZATION")
    savedToken = Token.objects.filter(token = currentToken).exists()
    if not savedToken:
        return False
    return True
