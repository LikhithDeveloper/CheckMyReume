from rest_framework import serializers
from .models import CustomUser,ResumeStorage, ResumeScoreStorage
from django.contrib.auth import get_user_model
import uuid

# User = get_user_model

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        feilds = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    email_token = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['name','email','password','phone_number','email_token','profile_image']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            name=validated_data['name'],
            email=validated_data['email'],
            phone_number=validated_data.get('phone_number'),
            email_token = str(uuid.uuid4()),
            profile_image = validated_data.get('profile_image')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField() 


class ResumeStorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeStorage
        fields = '__all__'

class ResumeScoreStorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeScoreStorage
        fields = '__all__'