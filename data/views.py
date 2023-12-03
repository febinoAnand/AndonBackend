import json
from rest_framework import viewsets, status, views
from rest_framework.response import Response
from .models import RawData, ProblemData, LastProblemData
from .serializers import RawSerializer, ProblemDataSerializer, LastProblemDataSerializer, RawSerializerWithDateTime
from events.models import Event, EventGroup
from events.serializers import EventSerializer
from devices.models import Device, Machine, Token
import datetime
from django.core import serializers


class RawGetMethod(views.APIView):
    schema = None
    def get(self,request):
        currentRawData = RawData.objects.all().order_by('-pk')
        jsonRawData = serializers.serialize('json', currentRawData)

        # rawDataSerializer = RawSerializerWithDateTime(currentRawData,many=True)

        # print (rawDataSerializer.data['datetime'])

        # updateDateTime = {'datetime':'testing'}
        # updateDateTime.update(rawDataSerializer.data)

        # return Response(rawDataSerializer.data, status=status.HTTP_201_CREATED)
        return Response(json.loads(jsonRawData), status=status.HTTP_201_CREATED)

class LiveDataViewset(views.APIView):
    schema = None

    def get(self,request):
        responseArray = []
        machines = Machine.objects.all()
        for machine in machines:
            print (machine)
            machineEvent = {}
            machineEvent["machineID"] = machine.machineID
            try:
                currentMachineProblem = ProblemData.objects.filter(machineID=machine).order_by('-pk')[0]
                currentEvent = Event.objects.get(eventID = currentMachineProblem.eventID)
                currentEventSerializer = EventSerializer(currentEvent,many=False)
                jsonCurrentEvent = json.dumps(currentEventSerializer.data)
                machineEvent['event'] = json.loads(jsonCurrentEvent)
            except IndexError as indexerr:
                machineEvent['event'] = {}
            except Exception as e:
                machineEvent['event'] = {}
                print(e)
            responseArray.append(machineEvent)


        print (responseArray)
        return Response(responseArray,status=status.HTTP_200_OK)
        # return Response({"status":"working fine"},status=status.HTTP_200_OK)


# Create your views here.
class RawDataViewset(viewsets.ModelViewSet):
    serializer_class = RawSerializer
    queryset = RawData.objects.all()
    http_method_names = ['post']

    def create(self,request,*args,**kwargs):
        res = request.body
        # print (res)

        # if not RawSerializer(data=request.data).is_valid():
        #     errorJson = {"status":"Not valid JSON"}
        #     return Response(errorJson,status=status.HTTP_201_CREATED)

        try:

            #sample ---- > {"date": "2023-08-26","time": "08:26:17","eventID": "EVE103","machineID": "MAC101","eventGroupID": "EG100"}
            jsondata = json.loads(res)
            tokenString = request.META.get("HTTP_DEVICEAUTHORIZATION")
            currentToken = Token.objects.get(token = tokenString)
            currentEvent = Event.objects.get(eventID=jsondata["eventID"])
            currentGroup = EventGroup.objects.get(groupID = jsondata['eventGroupID'])
            currentMachine = Machine.objects.get(machineID = jsondata['machineID'])
            currentDevice = Device.objects.get(deviceID=currentToken.deviceID)


            # for event in currentGroup.events:
            #     if event == currentEvent:

            #TODO validate event and eventGroup

            # if currentToken == None:
            #     errorJson = {"status":"Authentication Error. Add Token in the header in a name of 'DEVICEAUTHORIZATION'"}
            #     return Response(errorJson,status=status.HTTP_201_CREATED)


            # savedToken = Token.objects.get(deviceID = currentDevices)
            # if not currentToken == savedToken.token:
            #     errorJson = {"status":"Authentication Error. Invalid Token"}
            #     return Response(errorJson,status=status.HTTP_201_CREATED)


            # print (currentEvents)
            # print (currentDevices)
            # print (currentGroup)

            RawData.objects.create(
                        date = jsondata['date'],
                        time = jsondata['time'],
                        eventID = currentEvent,
                        deviceID = currentDevice,
                        machineID = currentMachine,
                        eventGroupID = currentGroup,
                        data = jsondata
                    )

            # currentMachine = Machine.objects.get(device = currentDevice)
            # print ("CurrentMachine--", currentMachine)


            eventTime = jsondata['date'] +" "+ jsondata['time']
            resEventTime = datetime.datetime.strptime(eventTime,"%Y-%m-%d %H:%M:%S")
            # print (resEventTime)

            # currentEventGroup = EventGroup.objects.filter(events__in = [currentEvents])
            # print ("currentEventGroup--", currentEventGroup)

            currentEventProblemType = currentEvent.problem.problemType
            # print ("currentEventProblemType---",currentEventProblemType)

            try:
                currentProbleData = ProblemData.objects.filter(eventGroupID = currentGroup, deviceID = currentDevice).order_by('-id')[0]
                # print("currentProbleDataIssueTime",currentProbleData.issueTime)
                # print("currentProbleDataEndTime",currentProbleData.endTime)
            except Exception as e:
                currentProbleData = None
                # print(e)


            if currentEventProblemType == "FINE":
                LastProblemData.objects.create(
                            date = jsondata['date'],
                            time = jsondata['time'],
                            eventID = currentEvent,
                            eventGroupID = currentGroup,
                            machineID = currentMachine,
                            deviceID = currentDevice,
                            endTime = resEventTime,
                        )

                if currentProbleData is not None and currentProbleData.endTime == None :
                    currentProbleData.eventID = currentEvent
                    currentProbleData.endTime = resEventTime
                    currentProbleData.save()



            elif currentEventProblemType == "ACKNOWLEDGE":
                LastProblemData.objects.create(
                    date = jsondata['date'],
                    time = jsondata['time'],
                    eventID = currentEvent,
                    eventGroupID = currentGroup,
                    machineID = currentMachine,
                    deviceID = currentDevice,
                    acknowledgeTime = resEventTime,
                )

                if currentProbleData is not None and currentProbleData.acknowledgeTime == None:
                    currentProbleData.acknowledgeTime = resEventTime
                    currentProbleData.save()

            else:
                LastProblemData.objects.create(
                    date = jsondata['date'],
                    time = jsondata['time'],
                    eventID = currentEvent,
                    eventGroupID = currentGroup,
                    machineID = currentMachine,
                    deviceID = currentDevice,
                    issueTime = resEventTime,
                )


                if currentProbleData == None or currentProbleData.endTime is not None:
                    ProblemData.objects.create(
                        date = jsondata['date'],
                        time = jsondata['time'],
                        eventID = currentEvent,
                        eventGroupID = currentGroup,
                        machineID = currentMachine,
                        deviceID = currentDevice,
                        issueTime = resEventTime,
                    )
                elif currentProbleData is not None or currentProbleData.endTime is None:
                    currentProbleData.date = jsondata['date']
                    currentProbleData.time = jsondata['time']
                    currentProbleData.eventID = currentEvent
                    currentProbleData.issueTime = resEventTime
                    currentProbleData.save()


            jsonResponse = {"data":"Success"}
            return Response(jsonResponse, status=status.HTTP_201_CREATED)
        except Exception as a:
            # print (a)
            # print("Not valid Json")
            RawData.objects.create(
                data = res
            )
            errorJson = {"data":"Not valid","error":str(a)}
            return Response(errorJson,status=status.HTTP_201_CREATED)


    # def create(self,request,*args,**kwargs):
    #     res = request.data
    #     # print (res)
    #
    #     try:
    #         jsondata = json.dumps(res["data"])
    #         RawData.objects.create(
    #             data = jsondata
    #         )
    #         return Response(res,status=status.HTTP_201_CREATED)
    #     except Exception as e:
    #         print("Not valid Json")
    #         RawData.objects.create(
    #             data = res
    #         )
    #         errorJson = {"data":"Not valid"}
    #         return Response(errorJson,status=status.HTTP_201_CREATED)


class ProblemViewSet(viewsets.ModelViewSet):
    schema = None
    serializer_class = ProblemDataSerializer
    queryset = ProblemData.objects.all().order_by('-pk')

class LastProblemViewSet(viewsets.ModelViewSet):
    schema = None
    serializer_class = LastProblemDataSerializer
    queryset = LastProblemData.objects.all().order_by('-pk')

