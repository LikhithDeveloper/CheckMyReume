from django.shortcuts import render,HttpResponse
from rest_framework.response import Response
from rest_framework import status
from .serializer import *
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate,login,logout
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.views.decorators.csrf import csrf_exempt
# import uuid
from .utils import *


class RegisterView(APIView):
    permission_classes = [AllowAny]
    # parser_classes = [MultiPartParser, FormParser, JSONParser]
    def post(self,request):
        serializer = RegisterSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        email = serializer.data['email']
        email_token = serializer.data['email_token']
        send_email_token(email,email_token)
        return Response(serializer.data)
    
    def get(self,request):
        user = CustomUser.objects.all()
        serializer = RegisterSerializer(user,many = True)
        return Response(serializer.data)
    
class LoginView(APIView):

    permission_classes = [AllowAny]
    def post(self,request):
        email = request.data['email']
        password = request.data['password']

        # user = CustomUser.objects.get(email = email)
        if not email or not password:
            raise AuthenticationFailed("Email and password are required")

        user = authenticate(request, email = email,password = password)
        login(request,user)
        if user is None:
            raise AuthenticationFailed("Invalid Credenrials")

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        })
    
class LogoutView(APIView):
    @csrf_exempt  # Disable CSRF for this view (not recommended)
    def post(self,request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
    
class ProtectedDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {"message": "This is protected data accessible to authenticated users only."}
        return Response(data)
    

def Verify(request,email_token):
    try:
        obj = CustomUser.objects.filter(email_token = email_token).first()
        obj.verified = True
        obj.save()
        return HttpResponse("Your account verified")

    except Exception as e:
        return HttpResponse("Invalid token")