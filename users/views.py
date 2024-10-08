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


from rest_framework.authentication import SessionAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To disable CSRF check


class RegisterView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    authentication_classes = [CsrfExemptSessionAuthentication]  # Use custom authentication
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
    authentication_classes = [CsrfExemptSessionAuthentication]  # Use custom authentication
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
    authentication_classes = [CsrfExemptSessionAuthentication]  # Use custom authentication
    # @csrf_exempt  # Disable CSRF for this view (not recommended)
    def post(self,request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
    
class ProtectedDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {"message": "This is protected data accessible to authenticated users only."}
        return Response(data)
    

class ResumeStorageView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CsrfExemptSessionAuthentication]  # Use custom authentication


    # @csrf_exempt
    def post(self,request):
        request.data['user'] = request.user.id
        # print(request.user.id)
        serializer = ResumeStorageSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Resume uploded succesfully"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request):
        resume = ResumeStorage.objects.filter(user = request.user.id)
        if resume:
            serializer = ResumeStorageSerializer(resume,many = True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({"message":"No resume found"}, status=status.HTTP_404_NOT_FOUND)
    def delete(self,request):
        item = request.data
        id = item.get('id')
        # print(id)
        resume = ResumeStorage.objects.get(id = id)
        if resume:
            resume.delete()  # Delete the resume instance
            return Response({"message": "Resume deleted successfully"}, status=status.HTTP_200_OK)
        return Response({"message": "No resume found"}, status=status.HTTP_404_NOT_FOUND)
    



class ResumeScoreStorageView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self,request):
        request.data['user'] = request.user.id
        serializer = ResumeScoreStorageSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response({"message":"Resume score not found"},status=status.HTTP_404_NOT_FOUND)
    
    def get(self,request):
        score = ResumeScoreStorage.objects.filter(user = request.user.id)
        if score:
            serializer = ResumeScoreStorageSerializer(score,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({"message":"Scores not found"},status=status.HTTP_404_NOT_FOUND)
    
    def delete(self,request):
        id = request.data.get('id')
        resume_score = ResumeScoreStorage.objects.get(id = id)
        if resume_score:
            resume_score.delete()
            return Response({"message":"deleted successfully"},status=status.HTTP_200_OK)
        return Response({"message":"Resume score not found"},status=status.HTTP_404_NOT_FOUND)

def Verify(request,email_token):
    try:
        obj = CustomUser.objects.filter(email_token = email_token).first()
        obj.verified = True
        obj.save()
        return HttpResponse("Your account verified")

    except Exception as e:
        return HttpResponse("Invalid token")