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



#In this method teacher are allowed to create students 
class add_student(APIView):
    permission_classes = (IsAuthenticated,)
    @csrf_exempt
    def post(self, request):
        username = request.data.get("username")
        firstname = request.data.get("firstname")
        lastname = request.data.get("lastname")
        email = request.data.get("email")
        password = request.data.get("password")
        mobile = request.data.get("mobile")
        if check_blank_or_null([username,firstname,lastname,email,password,mobile]) == True and teacher.objects.filter(user=request.user).exists():
            if User.objects.filter(username=username, email=email).exists():
                return Response({"message": "Username already exists created",},status=HTTP_200_OK)
            else:
                user = User.objects.create_user(username=username,first_name=firstname,last_name=lastname,email=email,password=password)
                user.save()
                teacherO = students.objects.create()
                teacherO.user = user
                teacherO.mobile = mobile
                teacherO.save()
                return Response({"message": "Your profile sucessfully created"},status=HTTP_200_OK)
        else:
            return Response({"message": "All filled must be filled"},status=HTTP_200_OK)
        	

#In this method teacher are allowed to see all students 
class list_student(APIView):
    permission_classes = (IsAuthenticated, )
    @csrf_exempt
    def get(self, request):
        context = {}
        lis=[]
        if teacher.objects.filter(user=request.user).exists():
            for x in students.objects.all():
                lis.append({"username":x.user.username,"First Name":x.user.firstname, "last Name":x.user.last_name,"email":x.user.email,"mobile":x.mobile})
            context['student']=lis
            return Response(context,status=HTTP_200_OK)
        else:
            return Response({"message": "You ARe not allowed"},status=HTTP_200_OK)
            	





#In this method teacher are allowed to add students marks 
class add_student_marks(APIView):
    permission_classes = (IsAuthenticated,)
    @csrf_exempt
    def post(self, request):
        student_username = request.data.get("student_username")
        subject = request.data.get("subject")
        mark = request.data.get("mark")
        #the next line is for validations
        if teacher.objects.filter(user=request.user).exists() and User.objects.filter(user=student_username).exists() and check_blank_or_null([student_username,subject,mark])==True:
            user=User.objects.get(user=student_username)
            studentO = students.objects.get(user=user)
            markO=markes.objects.create(student=studentO,subject=subject,marks=mark)
            markO.save()
            return Response({"message": "Your profile sucessfully created"},status=HTTP_200_OK)
        else:
            return Response({"message": "Your profile sucessfully created"},status=HTTP_200_OK)


#In this method teacher are allowed see  there student marks by username
class view_student_marks(APIView):
    permission_classes = (IsAuthenticated,)
    @csrf_exempt
    def post(self, request):
        student_username = request.data.get("student_username")
        if teacher.objects.filter(user=request.user).exists() and User.objects.filter(user=student_username).exists() and check_blank_or_null([student_username,subject,mark])==True:
            user=User.objects.get(user=student_username)
            studentO = students.objects.get(user=user)
            context={}
            details = []
            for x in markes.objects.filter(student=studentO):
                details.append({"subject":x.subject,"mark":x.marks})
            context['student']=details             
            return Response({"message": context},status=HTTP_200_OK)
        else:
            return Response({"message": "Your profile sucessfully created"},status=HTTP_200_OK)
    


#In this method student are allowed see there Information

@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def student_info(request):
    cust=students.objects.get(user=request.user)
    context = {}
    context['username'] = cust.user.username
    context['first_name'] = cust.user.first_name
    context['last_name'] = cust.user.last_name
    context['email'] = cust.user.email
    context['mobile'] = cust.mobile
    mark = []
    for x in markes.objects.filter(student=cust):
        mark.append({"subject":x.subject,"mark":x.marks})
    context['mark']=mark
    return HttpResponse(json.dumps(context), content_type='application/json')
