from django.shortcuts import render
from rest_framework import viewsets,views
from .models import UnauthUser, UserDetail, Setting
from .serializers import *
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
import json
from django.conf import settings
from datetime import datetime, timedelta
from .models import UserDetail
from .models import Setting as UserAuthSetting

import uuid
import random


import smsgateway.integrations as SMSgateway

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


class UserAuthAPI(views.APIView):
    def get(self,request):
        # print(request.body)
        return HttpResponseNotFound()
    
    def post(self,request):
        # print(request.body)
        
        responseData = {}

        requestAppToken = ""


        # responseData["status"] = "INVALID"
        # responseData["message"] = "Not a valid data"
        # responseData["otp_resend_seconds"] = 50
        # responseData["session_id"] = "d888433f-f0a7-4eb8-8be7-734d3531cb66"
        # responseData["mobile_no"] = "+919790928992"
        
        
########################### POST FLOW ##################################

        #check valid Json data in request 
        jsondata = {}
        try:
            jsondata = json.loads(request.body)
        except Exception as e:
            print (e)                       #TODO : save the exception in Log File
            return HttpResponseNotFound()
        
        
        #check app_token valid with Settings...
        if "appToken" not in jsondata:
            return HttpResponseNotFound()
        
        if jsondata["appToken"] != settings.APP_TOKEN:
            return HttpResponseNotFound()


        #Validate the Post Data....
        userAuthSerializer = UserAuthAPISerializer(data=jsondata)
        if not userAuthSerializer.is_valid():
            return HttpResponseBadRequest()


        #getting currentDate and Time
        currentDate = datetime.now().strftime("%Y-%m-%d")
        currentTime = datetime.now().strftime("%H:%M:%S")
        currentDateTime = datetime.now()
        # print (currentDate,currentTime)

########################### POST FLOW  END HERE ##################################



########################### CHECKING USER ##################################

        # Initialize app setting models
        userAuthSetting = UserAuthSetting.objects.first()

        # Filter Mobile No and get email ID
        userDetailsList = UserDetail.objects.filter(mobile_no = jsondata['mobileno'])
        userCount = len(userDetailsList)

        existingUserEmail = ""
        existingUserMob = ""

        #################### Existing User ##########################
        if userCount > 0:
            print ("Existing User")
            # print(userDetailsList[0].extUser.email)
            existingUserEmail = userDetailsList[0].extUser.email
            existingUserMob = userDetailsList[0].mobile_no
            
            print("Given email->",jsondata["email"])
            print("email in db->",existingUserEmail)
            print ("Checking Email address....")

            # Existing User But email Registered Already by another mobile.... 
            if existingUserEmail != jsondata["email"]:
                print ("Given Email id already used by another mobileno")
                maskedEmail = maskEmail(existingUserEmail)
                print ("Mask email",maskedEmail)
                responseData["status"] = "INVALID"
                responseData["message"] = "Mobile No already registered with email "+maskedEmail
                return  JsonResponse(responseData)

            # Existing User But email Registered Already....

            # generate SessionID
            # generatedSessionID = gen
            
            # add or update unauth user table with 
            unAuthUser = UnauthUser.objects.filter(mobile_no = existingUserMob)
            isUnauthUserExist = unAuthUser.exists()
            print("IsUnauthUserExist->",isUnauthUserExist)
            if isUnauthUserExist:
                unAuthUser[0].createdatetime = currentDateTime
                unAuthUser[0].emailaddress = jsondata["email"]
                unAuthUser[0].session_id = generateUUID()
                unAuthUser[0].device_id = jsondata["deviceID"]



                

            


        #################### New User ###############################
        else:
            print ("new User")
            userDetailsList = UserDetail.objects.filter(extUser__email = jsondata['email'])
            userByUserCount = len(userDetailsList)
        
            #Email id exist for another user
            if userByUserCount > 0:
                print("Error:Email id Exist for the mobile")
                #mask mobile no
                maskedMobile = maskPhoneNumber(userDetailsList[0].mobile_no)
                
                responseData["status"] = "INVALID"
                responseData["message"] = "Email Id already registered with "+maskedMobile
                return  JsonResponse(responseData)

            #Check user has pending session...
            usersInUnauth = UnauthUser.objects.filter(mobile_no = jsondata["mobileno"])
            userCount = len(usersInUnauth)


            generatedSessionID = ""

            #New user with new Session
            if userCount == 0:

                print("New User with New Session")

                # generate seesionID
                generatedSessionID = generateUUID()
                

                # generate 5 digit OTP
                generatedOTP = generate_otp()
                

                # TODO uncomment this

                # update in the unauthuser
                unAuthUser = UnauthUser.objects.create(
                    mobile_no = jsondata["mobileno"],
                    otp = generatedOTP,
                    emailaddress = jsondata["email"],
                    session_id = generatedSessionID,
                    device_id = jsondata["deviceID"]
                )

                # call SMS Model to send
                SendOTPSMS(jsondata["mobileno"],generatedOTP)

                # send jsonresponse OTP, session token, OTP resend, OTP expiry time, exsisting user status
                responseData["status"] = "OK"
                responseData["OTP"] = generatedOTP
                responseData["session_id"] = generatedSessionID
                responseData["otp_resend_interval"] = userAuthSetting.OTP_resend_interval
                responseData["otp_expiry_time"] = userAuthSetting.OTP_valid_time
                responseData["is_existing_user"] = False

                return JsonResponse(responseData)
            
            #New user with already Session Created...
            else:
                print("New User with Old Session")

                unAuthUser = usersInUnauth[0]
                userOTPCalled = unAuthUser.otp_called
                OTPcallLimit = userAuthSetting.OTP_call_count

                print("OTPcallCount", OTPcallLimit)

                #checkout OTP Call Count exceed
                if not userOTPCalled > OTPcallLimit:
                    userOTPCalled += 1
                
                    #Generate OTP
                    generatedOTP = generate_otp()

                    #assigning oldSessionID
                    generatedSessionID = unAuthUser.session_id

                    #update date and Time, call count, OTP 
                    unAuthUser.createdatetime = datetime.now()
                    unAuthUser.otp_called = userOTPCalled
                    unAuthUser.otp = generatedOTP
                    unAuthUser.save()

                    # #call SMS model to Send OTP
                    # SendOTPSMS(jsondata["mobileno"],generatedOTP)

                    # #send JSON response
                    # responseData["status"] = "OK"
                    # responseData["OTP"] = generatedOTP
                    # responseData["session_id"] = unAuthUser.session_id
                    # responseData["otp_resend_interval"] = userAuthSetting.OTP_resend_interval
                    # responseData["otp_expiry_time"] = userAuthSetting.OTP_valid_time
                    # responseData["is_existing_user"] = False

                    # return JsonResponse(responseData)
                
                #user Exceed retry 
                else:
                    print("OTP Call Count Exceed")
                    unAuthUserCreatedTime = unAuthUser.createdatetime
                    calculated_time = compareAndGetSeconds(unAuthUserCreatedTime,currentDateTime)

                    print("Time in seconds->",calculated_time)
                    print("Setting Seconds->",userAuthSetting.unAuth_user_expiry_time)

                    if calculated_time < userAuthSetting.unAuth_user_expiry_time:
                        responseData["status"] = "INVALID"
                        responseData["message"] = "Tried Too many times. Try after 15min Or Try Different Mobile number"
                        return JsonResponse(responseData)
                    
                    # generate new Session ID
                    generatedSessionID = generateUUID()

                    #reset OTP call count
                    userOTPCalled = 0

                    # Generate OTP
                    generatedOTP = generate_otp()

                    #update date and Time ,call count, OTP, session ID 
                    unAuthUser.createdatetime = datetime.now()
                    unAuthUser.otp_called = userOTPCalled
                    unAuthUser.otp = generatedOTP
                    unAuthUser.session_id = generatedSessionID
                    unAuthUser.save()

                #call SMS model to Send OTP
                SendOTPSMS(jsondata["mobileno"],generatedOTP)

                #send JSON response
                responseData["status"] = "OK"
                responseData["OTP"] = generatedOTP
                responseData["session_id"] = generatedSessionID
                responseData["otp_resend_interval"] = userAuthSetting.OTP_resend_interval
                responseData["otp_expiry_time"] = userAuthSetting.OTP_valid_time
                responseData["is_existing_user"] = False

                return JsonResponse(responseData)
                

                    
        return JsonResponse(responseData)
    

def maskEmail(email):
    parts = email.split("@")
    if len(parts) == 2:
        username, domain = parts
        masked_username = username[0:2] + '*'*(len(username)-4) + username[-2:]
        masked_domain = "*"+domain[1] + '*'*(len(domain)-3) + domain[-1]
        masked_email = masked_username + "@" + masked_domain
        return masked_email



def maskPhoneNumber(mobileNo):
    masked_number = mobileNo[:5] + '*'*(len(mobileNo)-6) + mobileNo[-2:]
    return masked_number

def generate_otp():
    otp = ""
    for _ in range(5):
        otp += str(random.randint(0, 9))
    return otp


def SendOTPSMS(number,OTPno):
    otpmessage = "Verification Code: {OTP}".format(OTP= OTPno)
    print ("OTP Sent",otpmessage)
    # SMSgateway.sendSMS(number,otpmessage)

def compareAndGetSeconds(fromDateTime,toDateTime):
    return (toDateTime - fromDateTime).total_seconds()


def generateUUID():
    return str(uuid.uuid4())