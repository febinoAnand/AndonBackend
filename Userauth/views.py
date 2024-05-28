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
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.conf import settings
import json
import uuid
import random
from rest_framework.authtoken.models import Token
from rest_framework import generics
from .serializers import GroupSerializer
from rest_framework import status
from pushnotification.models import Setting

from django.contrib.auth.models import Group
from django.contrib.auth.models import User  
from .serializers import UserSerializer

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
        existingUserDeviceID = ""

        #################### Existing User ##########################
        if userCount > 0:
            print ("Existing User")

            # print(userDetailsList[0].extUser.email)
            existingUserEmail = userDetailsList[0].extUser.email
            existingUserMob = userDetailsList[0].mobile_no
            existingUserDeviceID = userDetailsList[0].device_id
            
            print("Given email->",jsondata["email"])
            print("email in db->",existingUserEmail)
            print ("Checking Email address....")

            # Existing User But email was Registered Already by another mobile.... 
            if existingUserEmail != jsondata["email"]:
                print ("Given Email id already used by another mobileno")
                maskedEmail = maskEmail(existingUserEmail)
                print ("Mask email",maskedEmail)
                responseData["status"] = "INVALID"
                responseData["message"] = "Mobile Number already registered with "+maskedEmail
                return  JsonResponse(responseData)

            # Existing User But email Registered Already....

            # add or update unauth user table with 
            unAuthUser = UnauthUser.objects.filter(mobile_no = existingUserMob)
            isUnauthUserExist = unAuthUser.exists()
            
            generatedSessionID = generateUUID()
            # OTP_call_count = unAuthUser.otp_called

            print("IsUnauthUserExist->",isUnauthUserExist)
            
            if not isUnauthUserExist:    
                print("creating new user in unauth user")
                unAuthUser = UnauthUser(
                    mobile_no = existingUserMob,
                    emailaddress = existingUserEmail,
                    createdatetime = datetime.now(),
                    device_id = jsondata["deviceID"],
                    otp_called = 0,
                    is_existing_user = True,
                    session_id = generatedSessionID
                )            
                
            else:
                print("updating user in unauth user")
                unAuthUser = unAuthUser[0]
                unAuthUser.emailaddress = jsondata["email"]
                unAuthUser.device_id = jsondata["deviceID"]
                unAuthUser.save()

            OTP_call_count = unAuthUser.otp_called
            
            OTP_call_count += 1

            if OTP_call_count > userAuthSetting.OTP_call_count:

                secondsBetweenTime = compareAndGetSeconds(unAuthUser.createdatetime,currentDateTime)
                print("seconds->",secondsBetweenTime)
                print("settings seconds ->",userAuthSetting.unAuth_user_expiry_time)
                if not secondsBetweenTime > userAuthSetting.unAuth_user_expiry_time:
                    responseData["status"] = "INVALID"
                    responseData["message"] = "Tried Too many times. Try after {minutes}min".format(minutes=int(userAuthSetting.unAuth_user_expiry_time/60))
                    return JsonResponse(responseData)
                else:
                    OTP_call_count = 0
                    OTP_call_count += 1
                

            unAuthUser.createdatetime = currentDateTime
            unAuthUser.session_id = generatedSessionID
            unAuthUser.otp_called = OTP_call_count
            unAuthUser.save()

            # existingUserDeviceID = jsondata["deviceID"]
            if existingUserDeviceID != jsondata["deviceID"]:
                responseData["status"] = "PROMPT"
                responseData["message"] = "Already this user was registered. Do you want re-register?"
                responseData["session_id"] = generatedSessionID
                return JsonResponse(responseData)

            
            generatedOTP = generate_otp()    
            
            unAuthUser.otp = generatedOTP
            unAuthUser.save()

            # call SMS Model to send
            SendOTPSMS(jsondata["mobileno"],generatedOTP)
            
            responseData["status"] = "OK"
            responseData["session_id"] = generatedSessionID
            responseData["otp_resend_interval"] = userAuthSetting.OTP_resend_interval
            responseData["otp_expiry_time"] = userAuthSetting.OTP_valid_time
            responseData["is_existing_user"] = unAuthUser.is_existing_user

            return JsonResponse(responseData)




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
                # responseData["OTP"] = generatedOTP
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
                
                #increment OTP Call count
                userOTPCalled += 1
                
                
                #checkout OTP Call Count exceed
                if not userOTPCalled >= OTPcallLimit:
                    
                
                    #Generate OTP
                    generatedOTP = generate_otp()

                    #assigning oldSessionID
                    generatedSessionID = unAuthUser.session_id

                    #update date and Time, call count, OTP 
                    unAuthUser.createdatetime = datetime.now()
                    unAuthUser.otp_called = userOTPCalled
                    unAuthUser.otp = generatedOTP
                    unAuthUser.emailaddress = jsondata["email"]
                    unAuthUser.save()

                #user Exceed retry 
                else:
                    print("OTP Call Count Exceed")
                    unAuthUserCreatedTime = unAuthUser.createdatetime
                    calculated_time = compareAndGetSeconds(unAuthUserCreatedTime,currentDateTime)

                    print("Time in seconds->",calculated_time)
                    print("Setting Seconds->",userAuthSetting.unAuth_user_expiry_time)

                    if calculated_time < userAuthSetting.unAuth_user_expiry_time:
                        responseData["status"] = "INVALID"
                        responseData["message"] = "Tried Too many times. Try after {minute}min Or Try Different Mobile number".format(minute=int(userAuthSetting.unAuth_user_expiry_time/60))
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
                # responseData["OTP"] = generatedOTP
                responseData["session_id"] = generatedSessionID
                responseData["otp_resend_interval"] = userAuthSetting.OTP_resend_interval
                responseData["otp_expiry_time"] = userAuthSetting.OTP_valid_time
                responseData["is_existing_user"] = False

                return JsonResponse(responseData)
                    
        
    

class UserAuthPrompt(views.APIView):
    
    def get(self,request):
        # print(request.body)
        return HttpResponseNotFound()
    
    def post(self,request):
        # print(request.body)
        
        
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
        userAuthSerializer = UserAuthPromptSerializer(data=jsondata)
        if not userAuthSerializer.is_valid():
            return HttpResponseBadRequest()


        #getting currentDate and Time
        currentDate = datetime.now().strftime("%Y-%m-%d")
        currentTime = datetime.now().strftime("%H:%M:%S")
        currentDateTime = datetime.now()
        # print (currentDate,currentTime)

        ########################### POST FLOW  END HERE ##################################

        # initialize unauth user 
        responseData = {}
        userAuthSetting = UserAuthSetting.objects.first()
        unAuthUser = UnauthUser.objects.filter(session_id = jsondata["sessionID"])

        #check session id 
        if not len(unAuthUser) > 0:
            print("Session not found")
            responseData["status"] = "INVALID"
            responseData["message"] = "Session Expired Try again"
            return  JsonResponse(responseData)
        
        unAuthUser = unAuthUser[0]
        #compare device id
        if unAuthUser.device_id != jsondata["deviceID"]:
            print("Session Found device not match")
            unAuthUser.delete()
            responseData["status"] = "INVALID"
            responseData["message"] = "Device Mismatch. Try again"
            return  JsonResponse(responseData)

        #calculate time between createat and currentdatetime
        timeDifferenceInSeconds = compareAndGetSeconds(unAuthUser.createdatetime,currentDateTime)
        if timeDifferenceInSeconds > userAuthSetting.unAuth_user_expiry_time:
            print("Session Found but expired")
            unAuthUser.delete()
            responseData["status"] = "INVALID"
            responseData["message"] = "Session Expired Try again"
            return  JsonResponse(responseData)
        
        #check OTP count 
        if unAuthUser.otp_called > userAuthSetting.OTP_call_count:
            responseData["status"] = "INVALID"
            responseData["message"] = "Tried Too many times. Try after sometime"
            return JsonResponse(responseData)

        #checkpost data need to change
        if jsondata["needtochange"] != True:
            unAuthUser.delete()
            responseData["status"] = "OK"
            responseData["message"] = "Registration cancelled"
            return  JsonResponse(responseData)

        # generate OTP
        generatedOTP = generate_otp()

        # update otp in the 
        unAuthUser.otp = generatedOTP
        unAuthUser.createdatetime = currentDateTime

        # call SMS api
        SendOTPSMS(unAuthUser.mobile_no,generatedOTP)
        
        # send response
        responseData["status"] = "OK"
        responseData["session_id"] = jsondata["sessionID"]
        responseData["otp_resend_interval"] = userAuthSetting.OTP_resend_interval
        responseData["otp_expiry_time"] = userAuthSetting.OTP_valid_time
        return JsonResponse(responseData)
    

class UserVerifyView(views.APIView):
    def get(self,request):
        # print(request.body)
        return HttpResponseNotFound()
    
    def post(self,request):
        print(request.body)

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
        userAuthSerializer = UserAuthVerifySerializer(data=jsondata)
        if not userAuthSerializer.is_valid():
            return HttpResponseBadRequest()


        #getting currentDate and Time
        currentDate = datetime.now().strftime("%Y-%m-%d")
        currentTime = datetime.now().strftime("%H:%M:%S")
        currentDateTime = datetime.now()
        # print (currentDate,currentTime)

        ########################### POST FLOW  END HERE ##################################


        # initialize unauth user 
        responseData = {}
        userAuthSetting = UserAuthSetting.objects.first()
        unAuthUser = UnauthUser.objects.filter(session_id = jsondata["sessionID"])

        #check session id 
        if not len(unAuthUser) > 0:
            print("Session not found")
            responseData["status"] = "INVALID"
            responseData["message"] = "Session Expired Try again"
            return  JsonResponse(responseData)
        
        
        unAuthUser = unAuthUser[0]
        #compare device id
        if unAuthUser.device_id != jsondata["deviceID"]:
            print("Session Found device not match")
            unAuthUser.delete()
            responseData["status"] = "INVALID"
            responseData["message"] = "Device Mismatch. Try again"
            return  JsonResponse(responseData)

        #calculate time between createat and currentdatetime
        timeDifferenceInSeconds = compareAndGetSeconds(unAuthUser.createdatetime,currentDateTime)
        if timeDifferenceInSeconds > userAuthSetting.unAuth_user_expiry_time:
            print("Session Found but expired")
            unAuthUser.delete()
            responseData["status"] = "INVALID"
            responseData["message"] = "Session Expired Try again"
            return  JsonResponse(responseData)
        


        # Check OTP equals 
        OTP_Wrong_time = unAuthUser.otp_wrong_count
        if str(unAuthUser.otp) != jsondata["OTP"]:
            if OTP_Wrong_time > userAuthSetting.OTP_wrong_count:
                unAuthUser.delete()
                responseData["status"] = "INVALID"
                responseData["message"] = "OTP retry exceed. Try once again"
                return  JsonResponse(responseData)
            else:
                OTP_Wrong_time += 1
                unAuthUser.otp_wrong_count = OTP_Wrong_time
                unAuthUser.save()
                responseData["status"] = "INVALID"
                responseData["message"] = "OTP Wrong"
                return  JsonResponse(responseData)

        # Genereate verification ID
        generatedVerifiationID = generateUUID()
        unAuthUser.verification_token = generatedVerifiationID
        unAuthUser.save()

       
        try:
            setting = Setting.objects.first()
            if not setting:
                return Response({'error': 'No settings found'}, status=status.HTTP_404_NOT_FOUND)

            responseData = {
                "status": "OK",
                "session_id": request.data.get("sessionID"),
                "verification_id": generatedVerifiationID,  # replace this with your actual generated verification ID
                "Application_id": setting.application_id
            }

            return Response(responseData, status=status.HTTP_200_OK)
        except Setting.DoesNotExist:
            return Response({'error': 'Settings not found'}, status=status.HTTP_404_NOT_FOUND)
        
        


class UserRegisterView(views.APIView):
    def get(self,request):
        # print(request.body)
        return HttpResponseNotFound()
    
    def post(self,request):
        print(request.body)

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
        userAuthSerializer = UserAuthRegisterSerializer(data=jsondata)
        if not userAuthSerializer.is_valid():
            return HttpResponseBadRequest()


        #getting currentDate and Time
        currentDate = datetime.now().strftime("%Y-%m-%d")
        currentTime = datetime.now().strftime("%H:%M:%S")
        currentDateTime = datetime.now()
        # print (currentDate,currentTime)

        ########################### POST FLOW  END HERE ##################################
        
        # initialize unauth user 
        responseData = {}
        userAuthSetting = UserAuthSetting.objects.first()
        unAuthUser = UnauthUser.objects.filter(session_id = jsondata["sessionID"])
        

        #check session id 
        if not len(unAuthUser) > 0:
            print("Session not found")
            responseData["status"] = "INVALID"
            responseData["message"] = "Session Expired Try again"
            return  JsonResponse(responseData)
        
        unAuthUser = unAuthUser[0]
        userDetails = UserDetail.objects.filter(extUser__email=unAuthUser.emailaddress)


        #calculate time between createat and currentdatetime
        timeDifferenceInSeconds = compareAndGetSeconds(unAuthUser.createdatetime,currentDateTime)
        if timeDifferenceInSeconds > userAuthSetting.unAuth_user_expiry_time:
            print("Session Found but expired")
            unAuthUser.delete()
            responseData["status"] = "INVALID"
            responseData["message"] = "Session Expired Try again"
            return  JsonResponse(responseData)
        
        
        
        #compare device id
        if unAuthUser.device_id != jsondata["deviceID"]:
            print("Session Found device not match")
            unAuthUser.delete()
            responseData["status"] = "INVALID"
            responseData["message"] = "Device Mismatch. Try again"
            return  JsonResponse(responseData)
        
        if len(UserDetail.objects.filter(device_id = jsondata["deviceID"])):
            print("device already used by user")
            unAuthUser.delete()
            responseData["status"] = "INVALID"
            responseData["message"] = "Device Mismatch. Try again"
            return  JsonResponse(responseData)
        

        # Verify the verification token 
        if str(unAuthUser.verification_token) != jsondata["verificationID"]:
            print("usertable-->'"+unAuthUser.verification_token+"'")
            print("post-->'"+jsondata["verificationID"]+"'")
            unAuthUser.delete()
            responseData["status"] = "INVALID"
            responseData["session_id"] = "Not Verified Try process once again"
            return JsonResponse(responseData)
        
        # create or update user model with password
        # set inactive to the user
        # save deviceid and other details in userdetails
        if len(userDetails) > 0:
            for user in userDetails:
                print(user)

            userDetails = userDetails[0]
            userDetails.mobile_no = unAuthUser.mobile_no
            userDetails.designation = jsondata["designation"]
            userDetails.device_id = jsondata["deviceID"]
            userDetails.extUser.password = jsondata["password"]
            userDetails.extUser.first_name = jsondata["name"]
            userDetails.extUser.is_active = False
            userDetails.extUser.save()
            userDetails.save()  

        else:
            user = User.objects.create_user(
                                            username=unAuthUser.emailaddress, 
                                            email= unAuthUser.emailaddress, 
                                            password=jsondata["password"],
                                            )
            user.first_name = jsondata["name"]
            user.is_active = False
            user.save()
            
            userDetails = UserDetail.objects.create(
                extUser = user,
                designation = jsondata["designation"],
                mobile_no = unAuthUser.mobile_no,
                device_id = unAuthUser.device_id
            )
        
        # delete unauther user
        unAuthUser.delete()

        #send response
        responseData["status"] = "OK"
        responseData["session_id"] = jsondata["sessionID"]
        # responseData["verification_id"] = generatedVerifiationID
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

class ResendOTPView(views.APIView):
    def get(self,request):
        # print(request.body)
        return HttpResponseNotFound()
    def post(self, request):
        try:
            jsondata = json.loads(request.body)
        except Exception as e:
            print(e)
            return HttpResponseNotFound()

        required_fields = ["sessionID", "appToken"]
        if not all(field in jsondata for field in required_fields):
            return HttpResponseBadRequest("Missing required fields")

        if jsondata["appToken"] != settings.APP_TOKEN:
            return HttpResponseNotFound("Invalid app token")
        unauth_user = UnauthUser.objects.filter(session_id=jsondata["sessionID"]).first()

        # if not unauth_user:
        #     return HttpResponseNotFound("Session not found")
        response_data = {}
        if not unauth_user:
            response_data["status"] = "INVALID"
            response_data["message"] = "Session Expired Try again"
            return  JsonResponse(response_data)
        
        user_auth_setting = UserAuthSetting.objects.first()
        expiry_time = user_auth_setting.unAuth_user_expiry_time
        current_time = datetime.now()
        session_creation_time = unauth_user.createdatetime
        time_difference = (current_time - session_creation_time).total_seconds()

        if time_difference > expiry_time:
            response_data["status"] = "INVALID"
            response_data["message"] = "Session Expired Try again"
            return  JsonResponse(response_data)

        new_otp = generate_otp()
        unauth_user.otp = new_otp
        unauth_user.save()
        SendOTPSMS(unauth_user.mobile_no, new_otp)

        response_data = {
            "status": "OK",
            "message": "OTP resent successfully",
            "session_id": jsondata["session_id"],
            "otp_resend_interval": user_auth_setting.OTP_resend_interval,
            "otp_expiry_time": user_auth_setting.OTP_valid_time
        }
        return JsonResponse(response_data)
    





class RevokeAuthToken(APIView):
    def delete(self, request):
        token_key = request.query_params.get('token')

        if not token_key:
            return Response({'error': 'Token not provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the token exists
        try:
            token = Token.objects.get(key=token_key)
        except Token.DoesNotExist:
            return Response({'error': 'Token not found'}, status=status.HTTP_404_NOT_FOUND)

        # Delete the token
        token.delete()

        return Response({'message': 'Token revoked successfully'}, status=status.HTTP_204_NO_CONTENT)



class GroupUsersAPIView(APIView):
    def get(self, request, group_id):
        try:
            group = Group.objects.get(id=group_id)
            users = group.user_set.all()  
            serializer = UserSerializer(users, many=True)  
            return Response(serializer.data)
        except Group.DoesNotExist:
            return Response({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)
        

class GroupListView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer