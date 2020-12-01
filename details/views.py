from django.shortcuts import render
from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
import json
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from .models import teacher,students,markes,otp
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import HttpResponse
from rest_framework.response import Response
from django.contrib.auth.models import User
import math, random
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
import random
from django.core.mail import send_mail
from school.settings import EMAIL_HOST_USER
# Create your views here.




#this simple login view
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    password = request.data.get("password")
    username= request.data.get("username")
    print(username)
    print(password)
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        returnMessage = {'error': 'Invalid Credentials'}
        return HttpResponse(
        json.dumps(returnMessage),
        content_type = 'application/javascript; charset=utf8'
    )

    #this method create token or if exists in model it get token
    token, _ = Token.objects.get_or_create(user=user)
    returnToken = {'token':token.key}
    return HttpResponse(
        json.dumps(returnToken),
        content_type = 'application/javascript; charset=utf8'
    )

#this method generat otp for for verify otp
class forget_password(APIView):
    permission_classes = (AllowAny, )
    @csrf_exempt
    def post(self, request):
        username = request.POST.get("username")
        if check_blank_or_null([username]) ==True and User.objects.filter(username = username):
            user=User.objects.get(username=username)
            number=get_random_string(8)
            o,__=otp.objects.get_or_create(user=user)
            o.number=number
            o.save()
            send_mail('reset otp',OTP,EMAIL_HOST_USER,[user.email],fail_silently=False,)
            return Response({"message": "otp has been sent to your email"},status=HTTP_200_OK)
        else:
            return Response({"message": "email is not exists"},status=HTTP_200_OK)
    
#this method verify generated otp 
class verify_otp(APIView):
    permission_classes = (AllowAny, )
    @csrf_exempt
    def post(self, request):
        username = request.POST.get("username")
        otpO = request.POST.get("otp")
        password = request.POST.get("password")
        if check_blank_or_null([username]) ==True and User.objects.filter(username = username):
            user=User.objects.get(username=username)
            o=otp.objects.get(user=user)
            if o.otp ==otpO:
                user.password = password
                user.save()
                return Response({"message": "password successfully changed"},status=HTTP_200_OK)
            else:
                return Response({"message": "otp is not match"},status=HTTP_200_OK)    
        else:
            return Response({"message": "Username is not exists"},status=HTTP_200_OK)


#this is user for check the value if None or empty 
def check_blank_or_null(data):
    status = True
    for x in data:
        if x == "" and x == None:
            status = True
        else:
            pass
    return status        





#ITs simple signup page 
class signup(APIView):
    permission_classes = (AllowAny,)
    @csrf_exempt
    def post(self, request):
        username = request.data.get("username")
        firstname = request.data.get("firstname")
        lastname = request.data.get("lastname")
        email = request.data.get("email")
        password = request.data.get("password")
        mobile = request.data.get("mobile")
        if check_blank_or_null([username,firstname,lastname,email,password,mobile])==True:
            if User.objects.filter(username=username, email=email).exists():
                return Response({"message": "Username already exists created",},status=HTTP_200_OK)
            else:
                user = User.objects.create_user(username=username,first_name=firstname,last_name=lastname,email=email,password=password)
                user.save()
                teacherO = teacher.objects.create()
                teacherO.user = user
                teacherO.mobile = mobile
                teacherO.save()
                return Response({"message": "Your profile sucessfully created"},status=HTTP_200_OK)
        else:        
            return Response({"message": "All Filled must be filled"},status=HTTP_200_OK)


