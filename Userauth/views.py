from django.shortcuts import render
from rest_framework import viewsets
from .models import UnauthUser, UserDetail, Setting
from .serializers import UnauthUserSerializer, UserDetailSerializer, SettingSerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import DataSerializer

from django.shortcuts import get_object_or_404
from .models import UnauthUser

from .models import AuthTokenData


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



@api_view(['POST'])
def receive_api_data(request):
    if request.method == 'POST':
        serializer = DataSerializer(data=request.data)

        if serializer.is_valid():
            auth_token = serializer.validated_data.get('auth_token')
            mobile_number = serializer.validated_data.get('mobile_number')
            email = serializer.validated_data.get('email')
            dev_id = serializer.validated_data.get('dev_id')

            unauth_user = get_object_or_404(UnauthUser, verification_token=auth_token)

            if unauth_user:
                print("Auth Token:", auth_token)
                print("Mobile Number:", mobile_number)
                print("Email:", email)
                print("Device ID:", dev_id)

                
                AuthTokenData.objects.create(
                    auth_token=auth_token,
                    mobile_number=mobile_number,
                    email=email,
                    dev_id=dev_id
                )

                return Response({"message": "Data received and stored successfully!"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid auth token"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Only POST requests are allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
