from rest_framework import generics, status
from rest_framework.response import Response
from django.http import Http404, JsonResponse
from .models import Inbox, Settings, SearchParameter, UserEmailTracking, GroupEmailTracking
from .serializers import InboxSerializer, SettingsSerializer, SearchParameterSerializer , UserEmailTrackingSerializer ,GroupEmailTrackingSerializer ,GroupEmailSerializer
import logging
from django.shortcuts import get_object_or_404
import json
from django.contrib.auth.models import User, Group

logger = logging.getLogger(__name__)

class InboxView(generics.ListCreateAPIView):
    schema = None
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
    schema = None
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
    schema = None
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
        
class UserEmailTrackingAPIView(generics.ListCreateAPIView):
    schema = None
    queryset = UserEmailTracking.objects.all()
    serializer_class = UserEmailTrackingSerializer

    def get(self, request, *args, **kwargs):
        UserEmail_Tracking = self.get_queryset()
        serializer = self.get_serializer(UserEmail_Tracking, many=True)
        return Response(serializer.data)
    
class GroupEmailTrackingAPIView(generics.ListCreateAPIView):
    schema = None
    queryset = GroupEmailTracking.objects.all()
    serializer_class = GroupEmailTrackingSerializer

    def get(self, request, *args, **kwargs):
        GroupEmail_Tracking = self.get_queryset()
        serializer = self.get_serializer(GroupEmail_Tracking, many=True)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        try:
            res = request.data
            user_group = res.get('user_group')
            user_list_data = res.get('user_list')

            group, created = Group.objects.get_or_create(name=user_group)
            print(group)

            for user in user_list_data:
                user_list = User.objects.get(username=user)
                group.user_set.add(user_list)

            return JsonResponse({"status": "Ok"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        res = request.data
        try:

            jsondata = json.dumps(res)
            print("json data", jsondata)

            group_name = res.get('user_group')
            user_list_data = res.get('user_list')

            print("Group name-->",group_name)
            print("User list--->",user_list_data)

            groupModelobject = Group()
            groupModelobject.name = group_name
            groupModelobject.save()
            print("Group Model --->",groupModelobject)

            groupEmailTracking = GroupEmailTracking.objects.create(user_group = groupModelobject)
        

            # userListID = []
            for user in user_list_data:
                userObject = User.objects.get(username = user)
                print("User object",userObject)
                groupModelobject.user_set.add(userObject)
                groupEmailTracking.user_list.add(userObject)


                
                # userListID.append(userObject.pk)
            # print (userListID)
            # groupEmailTracking.user_list.set(userListID) 
            # groupEmailTracking.save()
                
            print (groupEmailTracking)
            
            # groupEmailTracking.save()
            # group = Group.objects.create(user_group=user_group_data)
            # group_email_tracking = GroupEmailTracking.objects.create(data=jsondata)
            # group_email_tracking.user_group.save(group)

            # for user_list in user_list_data:
            #     group_email_tracking.user_list.add(user_list)

            # group_email_tracking.save()
            

            # GroupEmailTracking.objects.create(
            #             user_group = usergroup,
            #             user_List = userlist,
            #             data = jsondata
            #         )
            return Response({"status":"Ok"},status=status.HTTP_201_CREATED)
        except Exception as a:
            print(a)
            errorJson = {"data":"Not valid","error":str(a)}
            return Response(errorJson,status=status.HTTP_201_CREATED)
        
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