from rest_framework import viewsets,status, views

from devices.serializers import MachineWithoutDeviceSerializer
from .models import *
from .serializers import *
from .models import *
from devices.models import Token, Device
from django.shortcuts import render
from rest_framework.response import Response

# Create your views here.
class ButtonViewSet(viewsets.ModelViewSet):
    serializer_class = ButtonSerializer
    queryset = Button.objects.all()
    schema = None

    def create(self, request, *args, **kwargs):
        res = request.data
        print (res)

        value = res['buttonDO']



        if value == '' or value == None or value == 0 or value == '0':
            value = 0

        else:
            buttonsWithDO = Button.objects.filter(buttonDO = value)
            print (buttonsWithDO)

            if (len(buttonsWithDO) >= 1):
                res = {"error":"DO already Assigned..."}
                return Response(res,status=status.HTTP_200_OK)
            # elif (len(buttonsWithDO) == 1) and buttonsWithDO[0]["buttonID"] != res['buttonID']:
            #     res = {"error":"DO already Assigned..."}
            #     return Response(res,status=status.HTTP_200_OK)


        button = Button.objects.create(
            buttonID =res["buttonID"],
            buttonName = res["buttonName"],
            buttonColor = res["buttonColor"],
            buttonColorName = res["buttonColorName"],
            buttonDO = value,
            buttonMode = res['buttonMode']
        )
        button.save()

        return Response(res,status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        res = request.data
        value = res['buttonDO']
        button = Button.objects.get(id=res['id'])
        if value == '' or value == None or value == 0 or value == '0':
            value = 0
        else:
            buttonDOlist = Button.objects.filter(buttonDO = value)
            if len(buttonDOlist) != 0 and buttonDOlist[0].id != button.id:
                res = {"error":"DO already Assigned"}
                return Response(res,status=status.HTTP_200_OK)

        button.buttonID = res['buttonID']
        button.buttonName = res['buttonName']
        button.buttonColor = res['buttonColor']
        button.buttonColorName = res['buttonColorName']
        button.buttonDO = value
        button.buttonMode = res['buttonMode']
        button.save()
        return Response(res,status=status.HTTP_200_OK)

    # http_method_names = ['get']

    # def list(self, request, *args, **kwargs):
    #
    #     if not authenticateDevice(request):
    #         errorJson = {"status":"Authentication Error. Invalid Token"}
    #         return Response(errorJson,status=status.HTTP_201_CREATED)
    #
    #     queryset = Button.objects.all()
    #     serializer = ButtonSerializer(queryset, many=True)
    #
    #     return Response(serializer.data,status=status.HTTP_200_OK)

class IndicatorViewSet(viewsets.ModelViewSet):
    serializer_class = IndicatorSerializer
    queryset = Indicator.objects.all()
    schema = None
    # http_method_names = ['get']

    # def list(self, request, *args, **kwargs):
    #
    #     if not authenticateDevice(request):
    #         errorJson = {"status":"Authentication Error. Invalid Token"}
    #         return Response(errorJson,status=status.HTTP_201_CREATED)
    #
    #     queryset = Indicator.objects.all()
    #     serializer = IndicatorSerializer(queryset, many=True)
    #
    #     return Response(serializer.data,status=status.HTTP_200_OK)

class ProblemCodeViewSet(viewsets.ModelViewSet):
    serializer_class = ProblemCodeSerializer
    queryset = ProblemCode.objects.all()
    schema = None
    # http_method_names = ['get']
    # def list(self, request, *args, **kwargs):
    #
    #     if not authenticateDevice(request):
    #         errorJson = {"status":"Authentication Error. Invalid Token"}
    #         return Response(errorJson,status=status.HTTP_201_CREATED)
    #
    #     queryset = ProblemCode.objects.all()
    #     serializer = ProblemCodeSerializer(queryset, many=True)
    #
    #     return Response(serializer.data,status=status.HTTP_200_OK)

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    schema = None
    # http_method_names = ['get']

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

        # if not authenticateDevice(request):
        #     errorJson = {"status":"Authentication Error. Invalid Token"}
        #     return Response(errorJson,status=status.HTTP_201_CREATED)

        queryset = Event.objects.all()
        serializer = EventSerializer(queryset, many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)


class EventGroupViewSet(viewsets.ModelViewSet):
    serializer_class = EventGroupSerializer
    queryset = EventGroup.objects.all()
    # http_method_names = ['get']
    schema = None

    def create(self, request, *args, **kwargs):
        res = request.data
        print ("Process Response", res)
        # authenticateDevice(res)

        eventGroup = EventGroup(groupID = res["groupID"])
        eventGroup.groupName = res["groupName"]

        events = res["eventSelectedValues"]
        machines = res["machineSelectedValues"]

        eventGroup.save()

        for event in events:
            currentEvent = Event.objects.get(eventID=event)
            eventGroup.events.add(currentEvent)

        for machine in machines:
            currentMachine = Machine.objects.get(machineID=machine)
            eventGroup.machines.add(currentMachine)

        eventGroup.save()
        return Response(res, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        res = request.data
        print(res)
        # authenticateDevice(res)

        eventGroup = EventGroup.objects.get(id=res['id'])
        events = res['eventSelectedValues']
        machines = res['machineSelectedValues']
        eventGroup.groupID = res["groupID"]
        eventGroup.groupName = res["groupName"]
        eventGroup.events.clear()
        eventGroup.machines.clear()
        eventGroup.save()

        for event in events:
            currentEvent = Event.objects.get(eventID=event)
            eventGroup.events.add(currentEvent)


        for machine in machines:
            currentMachine = Machine.objects.get(machineID=machine)
            eventGroup.machines.add(currentMachine)

        eventGroup.save()

        return Response(res, status=status.HTTP_200_OK)


    def list(self, request, *args, **kwargs):

        # if not authenticateDevice(request):
        #     errorJson = {"status":"Authentication Error. Invalid Token"}
        #     return Response(errorJson,status=status.HTTP_201_CREATED)

        queryset = EventGroup.objects.all()
        serializer = EventGroupSerializer(queryset, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class GetButtonView(views.APIView):

    def get(self,request):
        if not authenticateDevice(request):
            errorJson = {"status":"Authentication Error. Invalid Token"}
            return Response(errorJson,status=status.HTTP_201_CREATED)
        queryset = Button.objects.all()
        serializer = ButtonSerializer(queryset, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class GetIndicatorView(views.APIView):

    def get(self,request):
        if not authenticateDevice(request):
            errorJson = {"status":"Authentication Error. Invalid Token"}
            return Response(errorJson,status=status.HTTP_201_CREATED)
        queryset = Indicator.objects.all()
        serializer = IndicatorSerializer(queryset, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class GetProblemCodeView(views.APIView):

    def get(self,request):
        if not authenticateDevice(request):
            errorJson = {"status":"Authentication Error. Invalid Token"}
            return Response(errorJson,status=status.HTTP_201_CREATED)
        queryset = ProblemCode.objects.all()
        serializer = ProblemCodeSerializer(queryset, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class GetEventView(views.APIView):
    def get(self,request):
        if not authenticateDevice(request):
            errorJson = {"status":"Authentication Error. Invalid Token"}
            return Response(errorJson,status=status.HTTP_201_CREATED)
        queryset = Event.objects.all()
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class GetEventGroupView(views.APIView):
    def get(self,request):
        if not authenticateDevice(request):
            errorJson = {"status":"Authentication Error. Invalid Token"}
            return Response(errorJson,status=status.HTTP_201_CREATED)
        queryset = EventGroup.objects.all()
        serializer = EventGroupSerializer(queryset, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class GetMachineEventView(views.APIView):
    def get(self,request):
        if not authenticateDevice(request):
            errorJson = {"status":"Authentication Error. Invalid Token"}
            return Response(errorJson,status=status.HTTP_201_CREATED)
        deviceToken = request.META.get("HTTP_DEVICEAUTHORIZATION")
        currentDeviceToken = Token.objects.get(token=deviceToken)
        selectedDevice = Device.objects.get(deviceID = currentDeviceToken.deviceID)
        filteredMachines = Machine.objects.filter(device=selectedDevice)
        filterMachineSerializer = MachineEventsGroupSerializer(filteredMachines,many=True)

        return Response(filterMachineSerializer.data,status=status.HTTP_200_OK)




        # Working Code of get machine details filter with device
        # res = request.data
        # requestDevice = Device.objects.get(deviceID=res["deviceID"])
        # queryset = Machine.objects.filter(device=requestDevice)
        # machineSerializer = MachineWithoutDeviceSerializer(queryset,many=True)
        #
        # return Response(machineSerializer.data,status=status.HTTP_200_OK)




    # def get_serializer(self,selectedMachineEvent):
    #     querySet = EventGroup.objects.filter(groupID=selectedMachineEvent)
    #     eventSerializer = EventGroupSerializer(querySet,many=True)
    #     retData = eventSerializer.data
    #     return retData["json"]
    # if not authenticateDevice(request):
    #     errorJson = {"status":"Authentication Error. Invalid Token"}
    #     return Response(errorJson,status=status.HTTP_201_CREATED)


def authenticateDevice(data):
    currentToken = data.META.get("HTTP_DEVICEAUTHORIZATION")
    savedToken = Token.objects.filter(token = currentToken).exists()
    if not savedToken:
        return False
    return True
