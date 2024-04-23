import json
import math
import random

from rest_framework import viewsets, status, views

from rest_framework.response import Response
from .models import *
from .serializers import MachineSerializer, \
    DeviceSerializer, \
    RFIDSerializer, \
    UnRegisteredSerializer, \
    VerifyDeviceSerializer,\
    GetTokenSerializer,\
    UnRegisteredGetMethodSerializer
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
import uuid
from django.db.utils import IntegrityError
from django.core import serializers


# Create your views here.
class MachineViewSet(viewsets.ModelViewSet):
    serializer_class = MachineSerializer
    queryset = Machine.objects.all()
    schema = None


    def list(self,request, *args,**kwargs):
        queryset = Machine.objects.all().order_by("device__deviceID")
        serializers = MachineSerializer(queryset,many=True)
        # res = {"message":"working fine"}
        return Response(serializers.data,status=status.HTTP_200_OK)
    # def machine123(self,request,pk=None):
    #     res = {"message":"working fine"}
    #     return Response(res,status=status.HTTP_200_OK)



    def create(self,request,pk=None):
        # print(request.data)
        reqData = request.data
        # res = {"message":"working fine"}
        # hmiID = reqData["deviceID"]
        DeviceData = Device.objects.get(id=reqData["Device"]["id"])
        # print (hmiID)
        Machine.objects.create(machineID = reqData['machineID'],
                               name = reqData['name'],
                               manufacture = reqData['manufacture'],
                               model = reqData['model'],
                               line = reqData['line'],
                               device = DeviceData)

        return Response(reqData,status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        # print (request.data)
        res = request.data
        machine = Machine.objects.get(id=res["id"])
        machine.machineID=res["machineID"]
        machine.model = res["model"]
        machine.name = res["name"]
        machine.line = res["line"]
        machine.device = Device.objects.get(id=res["Device"]["id"])
        machine.manufacture = res["manufacture"]
        machine.save()
        return Response(res,status=status.HTTP_200_OK)


class DeviceViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceSerializer
    queryset = Device.objects.all()
    schema = None

class RFIDViewSet(viewsets.ModelViewSet):
    serializer_class = RFIDSerializer
    queryset = RFID.objects.all()

class UnRegisteredViewSet(viewsets.ModelViewSet):
    serializer_class = UnRegisteredSerializer
    queryset = UnRegisteredDevice.objects.all()
    http_method_names = ['get']
    schema = None
    # def list(self, request, *args, **kwargs):
    #     query = UnRegisteredDevice.objects.all()
    #     serializers_data = UnRegisteredGetMethodSerializer(query, many=True)
    #     return Response(serializers_data.data,status = status.HTTP_200_OK)


    # def create(self, request, *args, **kwargs):
    #     res = request.data
    #     print (res)
    #     generatedUUID = uuid.uuid4()
    #     generatedOTP = generateSixDigitOTP()
    #     print ("OTP--->",generatedOTP)
    #     print ("Session ID--->",generatedUUID)
    #
    #
    #     try:
    #         if Device.objects.filter(deviceID = res["deviceID"]).exists():
    #             jsonResponse = {"deviceID":res["deviceID"],"staus":"Device Already Registered"}
    #         else:
    #             UnRegisteredDevice.objects.create(
    #                 sessionID = generatedUUID,
    #                 deviceID = res["deviceID"],
    #                 devicePassword = res["devicePassword"],
    #                 model = res["model"],
    #                 hardwareVersion = res["hardwareVersion"],
    #                 softwareVersion = res["softwareVersion"],
    #                 OTP = generatedOTP
    #             )
    #             jsonResponse = {"deviceID":res["deviceID"],"sessionID":str(generatedUUID),"staus":"OTP was generated in the dashboard. Use sessionID to register the device"}
    #     except IntegrityError as Ie:
    #         jsonResponse = {"deviceID":res["deviceID"],"staus":"Device ID already Pending for Verification"}
    #
    #     return Response(jsonResponse,status=status.HTTP_201_CREATED)

class UnRegisterViewSetPostMethod(views.APIView):

    def get_serializer(self,*args, **kwargs):
        return UnRegisteredGetMethodSerializer(*args, **kwargs)

    def post(self,request):
        res = request.data
        print (res)

        generatedUUID = uuid.uuid4()
        generatedOTP = generateSixDigitOTP()

        # print ("OTP--->",generatedOTP)
        # print ("Session ID--->",generatedUUID)


        try:
            if Device.objects.filter(deviceID = res["deviceID"]).exists():
                jsonResponse = {"deviceID":res["deviceID"],"staus":"Device Already Registered"}
            else:
                UnRegisteredDevice.objects.create(
                    sessionID = generatedUUID,
                    deviceID = res["deviceID"],
                    devicePassword = res["devicePassword"],
                    model = res["model"],
                    hardwareVersion = res["hardwareVersion"],
                    softwareVersion = res["softwareVersion"],
                    OTP = generatedOTP
                )
                jsonResponse = {"deviceID":res["deviceID"],"sessionID":str(generatedUUID),"staus":"OTP was generated in the dashboard. Use sessionID to register the device"}
        except IntegrityError as Ie:
            jsonResponse = {"deviceID":res["deviceID"],"staus":"Device ID already Pending for Verification"}

        return Response(jsonResponse,status=status.HTTP_201_CREATED)


class TokenAuthentication(views.APIView):
    def get_serializer(self,*args, **kwargs):
        return GetTokenSerializer(*args, **kwargs)

    def post(self,request):
        res = request.data
        print (res)
        verifiyTokenSerializer = GetTokenSerializer(data=res)
        jsonResponse = {"status":"Not a Valid JSON"}
        if verifiyTokenSerializer.is_valid():
            try:
                currentDevice = Device.objects.get(deviceID = res['deviceID'])
            except Exception as e:
                jsonResponse = {"status":"Devive ID not Registered"}
                return Response(jsonResponse, status=status.HTTP_201_CREATED)

            jsonResponse = {"deviceID":currentDevice.deviceID,"status":"Invalid Credentials"}
            if currentDevice.devicePassword == res['devicePassword']:
                currentToken = Token.objects.get(deviceID=currentDevice)
                jsonResponse = {"deviceID":currentDevice.deviceID,"token":str(currentToken.token)}

        return Response(jsonResponse, status=status.HTTP_201_CREATED)


class DeviceVerification(views.APIView):

    def get_serializer(self, *args, **kwargs):
        return VerifyDeviceSerializer(*args, **kwargs)

    def post(self, request):
        res = request.data
        print (res)

        verifyDevice = VerifyDeviceSerializer(data=res)
        if verifyDevice.is_valid():
            try:
                currentUnRegisteredDevice = UnRegisteredDevice.objects.get(sessionID = res['sessionID'])
            except Exception as e:
                currentUnRegisteredDevice = None

            if currentUnRegisteredDevice is not None and str(currentUnRegisteredDevice.OTP) == res["OTP"]:


                registerDevice = Device.objects.create(
                    deviceID = currentUnRegisteredDevice.deviceID,
                    model = currentUnRegisteredDevice.model,
                    hardwareVersion = currentUnRegisteredDevice.hardwareVersion,
                    softwareVersion = currentUnRegisteredDevice.softwareVersion,
                    devicePassword = currentUnRegisteredDevice.devicePassword
                )
                registerDevice.save()
                genratedToken = generate_token()
                deviceToken = Token.objects.create(
                    deviceID = registerDevice,
                    token = genratedToken
                )
                deviceToken.save()
                currentUnRegisteredDevice.delete()
                jsonResponse = {"deviceID":currentUnRegisteredDevice.deviceID,"token":str(genratedToken),"status":"Device Successfully Verified"}
            elif currentUnRegisteredDevice == None:
                jsonResponse = {"status":"sessionID is not valid"}
            else:
                jsonResponse = {"status":"OTP is not valid"}
        else:
            jsonResponse = {"status":"Not a Valid Data"}

        return Response(jsonResponse, status=status.HTTP_201_CREATED)

# class TokenView(viewsets.ModelViewSet):


def generateSixDigitOTP():
    digits = [i for i in range(0, 10)]
    random_no = 0
    for i in range(6):
        index = math.floor(random.random() * 10)
        random_no += (digits[index] * pow(10,i))
    return random_no

def generate_token():
    return binascii.hexlify(os.urandom(20)).decode()
