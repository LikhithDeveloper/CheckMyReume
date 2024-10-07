from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
# Create your models here.


class CustomUser(AbstractUser):
    username = None
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100,unique=True)
    password = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=12)
    verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=200)
    profile_image = models.ImageField(upload_to="profile",null=True,blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class ResumeStorage(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    resume = models.FileField(upload_to="resume",null=True,blank=True)

    def __str__(self) -> str:
        return self.user.name
    

class ResumeScoreStorage(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    resume = models.CharField(max_length=100000,null=True,blank=True)
     
    