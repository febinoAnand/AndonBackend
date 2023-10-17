import json
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import RawData, ProblemData, LastProblemData
from .serializers import RawSerializer, ProblemDataSerializer, LastProblemDataSerializer
from events.models import Event, EventGroup
from devices.models import Device, Machine, Token
import datetime


# Create your views here.
class RawDataViewset(viewsets.ModelViewSet):
    serializer_class = RawSerializer
    queryset = RawData.objects.all()
    http_method_names = ['get','post']

    # def get_serializer(self, *args, **kwargs):
    #     return RawSerializer(*args, **kwargs)

    def create(self,request,*args,**kwargs):
        res = request.body
        print (res)

        # if not RawSerializer(data=request.data).is_valid():
        #     errorJson = {"status":"Not valid JSON"}
        #     return Response(errorJson,status=status.HTTP_201_CREATED)



        try:
            jsondata = json.loads(res)
            currentEvents = Event.objects.get(eventID=jsondata["eventID"])
            currentDevices = Device.objects.get(deviceID = jsondata['deviceID'])
            currentGroup = EventGroup.objects.get(groupID = jsondata['eventGroupID'])


            currentToken = request.META.get("HTTP_DEVICEAUTHORIZATION")

            # if currentToken == None:
            #     errorJson = {"status":"Authentication Error. Add Token in the header in a name of 'DEVICEAUTHORIZATION'"}
            #     return Response(errorJson,status=status.HTTP_201_CREATED)

            savedToken = Token.objects.get(deviceID = currentDevices)
            if not currentToken == savedToken.token:
                errorJson = {"status":"Authentication Error. Invalid Token"}
                return Response(errorJson,status=status.HTTP_201_CREATED)


            # print (currentEvents)
            # print (currentDevices)
            # print (currentGroup)

            RawData.objects.create(
                        date = jsondata['date'],
                        time = jsondata['time'],
                        eventID = currentEvents,
                        deviceID = currentDevices,
                        eventGroupID = currentGroup,
                        data = jsondata
                    )

            currentMachine = Machine.objects.get(device = currentDevices)
            # print ("CurrentMachine--", currentMachine)



            eventTime = jsondata['date'] +" "+ jsondata['time']
            resEventTime = datetime.datetime.strptime(eventTime,"%Y-%m-%d %H:%M:%S")
            # print (resEventTime)

            # currentEventGroup = EventGroup.objects.filter(events__in = [currentEvents])
            # print ("currentEventGroup--", currentEventGroup)

            currentEventProblemType = currentEvents.problem.problemType
            # print ("currentEventProblemType---",currentEventProblemType)

            try:
                currentProbleData = ProblemData.objects.filter(eventGroupID = currentGroup, deviceID = currentDevices).order_by('-id')[0]
                # print("currentProbleDataIssueTime",currentProbleData.issueTime)
                # print("currentProbleDataEndTime",currentProbleData.endTime)
            except Exception as e:
                currentProbleData = None
                # print(e)


            if currentEventProblemType == "FINE":
                LastProblemData.objects.create(
                            date = jsondata['date'],
                            time = jsondata['time'],
                            eventID = currentEvents,
                            eventGroupID = currentGroup,
                            machineID = currentMachine,
                            deviceID = currentDevices,
                            endTime = resEventTime,
                        )

                if currentProbleData is not None and currentProbleData.endTime == None :
                    currentProbleData.eventID = currentEvents
                    currentProbleData.endTime = resEventTime
                    currentProbleData.save()



            elif currentEventProblemType == "ACKNOWLEDGE":
                LastProblemData.objects.create(
                    date = jsondata['date'],
                    time = jsondata['time'],
                    eventID = currentEvents,
                    eventGroupID = currentGroup,
                    machineID = currentMachine,
                    deviceID = currentDevices,
                    acknowledgeTime = resEventTime,
                )

                if currentProbleData is not None and currentProbleData.acknowledgeTime == None:
                    currentProbleData.acknowledgeTime = resEventTime
                    currentProbleData.save()

            else:
                LastProblemData.objects.create(
                    date = jsondata['date'],
                    time = jsondata['time'],
                    eventID = currentEvents,
                    eventGroupID = currentGroup,
                    machineID = currentMachine,
                    deviceID = currentDevices,
                    issueTime = resEventTime,
                )


                if currentProbleData == None or currentProbleData.endTime is not None:
                    ProblemData.objects.create(
                        date = jsondata['date'],
                        time = jsondata['time'],
                        eventID = currentEvents,
                        eventGroupID = currentGroup,
                        machineID = currentMachine,
                        deviceID = currentDevices,
                        issueTime = resEventTime,
                    )
                elif currentProbleData is not None or currentProbleData.endTime is None:
                    currentProbleData.date = jsondata['date']
                    currentProbleData.time = jsondata['time']
                    currentProbleData.eventID = currentEvents
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
    serializer_class = ProblemDataSerializer
    queryset = ProblemData.objects.all()

class LastProblemViewSet(viewsets.ModelViewSet):
    serializer_class = LastProblemDataSerializer
    queryset = LastProblemData.objects.all()

