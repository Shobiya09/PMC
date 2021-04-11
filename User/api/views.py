from rest_framework import status
from rest_framework.response import Response

from django.views.decorators.csrf import csrf_exempt
from User.api.serializers import UserAuthenticaton,LoginSerializer,ChangepswSerializer,otpSerializer,otpvalidSerializer
from rest_framework.decorators import api_view
from User.models import Detail
#from rest_framework.authtoken.models import Token
#from django.contrib.auth import login as django_login

@csrf_exempt
@api_view(['GET', 'POST','PATCH'])
def register_view(request,*args, **kwargs):
    if  request.method == 'POST':
        serializer=UserAuthenticaton(data=request.data)
        d={}
        if serializer.is_valid():
            instance, created = Detail.objects.update_or_create(email=serializer.validated_data.get('email', None), defaults=serializer.validated_data)
            user=Detail.objects.get(email=serializer.data['email'])
            if not created:
                serializer.update(instance, serializer.validated_data)

                response={
                            "status_type": "true",
                            "entity": [
                                {
                                    "user_id": user.id
                                }
                            ],
                            "entity_type": "JsonArrays",
                            "entity_status": "1",
                            "entity_msg": "User is already exists and update user details successfully.",
                            "status": "200"
                        }
                return Response(response)
            response={
                        "status_type": "true",
                        "entity": [
                            {
                                "user_id": user.id
                            }
                        ],
                        "entity_type": "JsonArrays",
                        "entity_status": "1",
                        "entity_msg": "New user details registered successfully.",
                        "status": "200"
                    }
            return Response(response)
            #serializer.save()
            #d['response']='successfully registered'
        else:
            d=serializer.errors
        return Response(d,status=status.HTTP_202_ACCEPTED)

@csrf_exempt
@api_view(['POST'])
def login_view(request,*args, **kwargs):
    serializer=LoginSerializer(data=request.data)
    d={}
    if serializer.is_valid():
        user=Detail.objects.get(email=serializer.data['email'])
        response={
                        "status_type": "true",
                        "entity": [
                            {
                                "user_id": user.id
                            }
                        ],
                        "entity_type": "JsonArrays",
                        "entity_status": "1",
                        "entity_msg": "User login successfully.",
                        "status": "200"
                    }
        return Response(response)
    else:
        d=serializer.errors
    return Response(d,status=status.HTTP_202_ACCEPTED)

@csrf_exempt
@api_view(['POST'])
def update_view(request,*args, **kwargs):

    serializer=ChangepswSerializer(data=request.data)
    d={}
    if serializer.is_valid():

        instance=Detail.objects.get(email=serializer.data['email'])
        response={
                    "status_type": "true",
                    "entity": [
                        {
                            "user_id": instance.id
                        }
                    ],
                    "entity_type": "JsonArrays",
                    "entity_status": "1",
                    "entity_msg": "User new password is updated successfully.",
                    "status": "200"
                }
        return Response(response)
    else:
        d=serializer.errors
    return Response(d,status=status.HTTP_202_ACCEPTED)

@csrf_exempt
@api_view(['POST'])
def otp_view(request,*args, **kwargs):
    serializer=otpSerializer(data=request.data)
    if serializer.is_valid():
        user=Detail.objects.get(email=serializer.data['email'])
        response={
                        "status_type": "true",
                        "entity": [
                            {
                                "user_id": user.id
                       }
                        ],
                        "entity_type": "JsonArrays",
                        "entity_status": "1",
                        "entity_msg": "User OTP generator successfully.",
                        "status": "200"
                    }

        return Response(response)
    else:

        return Response(serializer.errors,status=status.HTTP_202_ACCEPTED)


@csrf_exempt
@api_view(['POST'])
def otpvalid_view(request,*args, **kwargs):
    serializer=otpvalidSerializer(data=request.data)
    if serializer.is_valid():
        user=Detail.objects.get(email=serializer.data['email'])
        response={
                        "status_type": "true",
                        "entity": [
                            {
                                "user_id": user.id
                       }
                        ],
                        "entity_type": "JsonArrays",
                        "entity_status": "1",
                        "entity_msg": "User login password changed successfully",
                        "status": "200"
                    }
        return Response(response)
    else:

        return Response(serializer.errors)
