from django.contrib import admin
from django.urls import path
from details.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login",login),
    path("forget_password",forget_password.as_view()),
    path("verify_otp",verify_otp.as_view()),
    path("signup",signup.as_view()),
    path("add_student",add_student.as_view()),
    path("list_student",list_student.as_view()),
    path("add_student_marks",add_student_marks.as_view()),
    path("view_student_marks",view_student_marks.as_view()),
    path("student_info",student_info)
]
