from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class teacher(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	mobile=models.CharField(default="9999999999",max_length=20)
	def __str__(self):
		return self.mobile



class students(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	mobile=models.CharField(default="9999999999",max_length=20)
	def __str__(self):
		return self.mobile


class markes(models.Model):
    student=models.ForeignKey(students,on_delete=models.CASCADE,null=True)
    subject=models.CharField(default="subject",max_length=50)
    marks=models.IntegerField(default=0)
    def __str__(self):
        return self.subject


class otp(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE, null=True)
	number=models.CharField(default=" ",max_length=50)
	def __str__(self):
		return self.number

