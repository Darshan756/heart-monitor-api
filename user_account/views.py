import email
from multiprocessing import Value
from urllib import request
from django.conf import settings
from django.forms import ValidationError
from django.shortcuts import render
from rest_framework import generics,viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from . import authentication
from .models import CustomUser
from .serializers import UserRegisterSerializer
from rest_framework import status
from .utils import send_link
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.middleware import csrf
from .authentication import CustomAuthentication 
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import exceptions
from django.contrib.auth.password_validation import validate_password

# Create your views here.



class UserRegisterView(APIView):
      authentication_classes = []  

      permission_classes = [AllowAny]
      def post(self,request):
            
            serializer = UserRegisterSerializer(data=request.data)
            if serializer.is_valid():
                  user = serializer.save()
                  subject = 'Activate Your Account'
                  template = 'user_account/user_activation_link.html'
                  try:
                        send_link(request, user, subject, template)
                  except Exception as e:
                        return Response({"error": f"Email could not be sent: {str(e)}"}, status=500)

                  return Response({'message':'Registration Successfull! please click the on link in your email to activate your account '},status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ActivationConfirmView(APIView):
      authentication_classes = []  

      def get(self,request,uidb64,token):
            try:
                  uid = urlsafe_base64_decode(uidb64).decode()
                  user = CustomUser.objects.get(id=uid)
            except CustomUser.DoesNotExist:
                  return Response({'message':"Invaid or expired Token"},status=status.HTTP_401_UNAUTHORIZED)
            if user is not None and default_token_generator.check_token(user,token):
                   user.is_active = True 
                   user.save()
                   return Response({'message':'activation successfull!','user':user.get_full_name()})
            return Response({'message':'Permission denied'},status=status.HTTP_403_FORBIDDEN)

class UserSigninView(APIView):
      authentication_classes = []  
      permission_classes = [AllowAny]
      def post(self,request):
            email = request.data.get('email')
            password = request.data.get('password')
            
            print(email)
            print(password)
            if not email or not password:
                  return Response({'message':'Please provide both email and password'},status=status.HTTP_400_BAD_REQUEST)
            user = authenticate(request,email=email,password=password)
            if user is None:
                  return Response({'error':'Invalid credentials!'},status=status.HTTP_401_UNAUTHORIZED) 
            
            refresh = RefreshToken.for_user(user=user)
            response = Response({
                  "message":"Login successfull"
            }) 
            response.set_cookie(
                  key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                  value=str(refresh),
                  secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                  httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                  samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                  path='/'
            )
            response.set_cookie(
                  key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                  value=str(refresh.access_token),
                  secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                  httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                  samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                  path='/'
            )
            csrf_token = csrf.get_token(request) 
            response['X-CSRFToken'] = csrf_token

            return response

class RefreshTokenView(APIView):
      authentication_classes = []  
      permission_classes = [AllowAny]
      def post(self,request):
            refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
            if not refresh_token:
                  return Response({'error':"Invalid or expired token"},status=status.HTTP_400_BAD_REQUEST)
            
            refresh = RefreshToken(refresh_token)
            response = Response({
                  'access':str(refresh.access_token),
                  
            },status=status.HTTP_200_OK)
            response.set_cookie(
                  key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                  value=str(refresh.access_token),
                  secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                  httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                  samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                  path='/'
            )
            response['X-CSRFToken'] = csrf.get_token(request)
            return response
      
class ResetPasswordView(APIView):
      authentication_classes = []
      permission_classes = [AllowAny]

      def post(self,request):
            email = request.data.get('email')
            if  email is None:
                  return Response({'error':'Please provide your email!'},status=status.HTTP_400_BAD_REQUEST)
            try:
                  user = CustomUser.objects.get(email=email)

            except CustomUser.DoesNotExist:
                  return Response({'error':'User with this email does not exist!'},status=status.HTTP_400_BAD_REQUEST)

         
            subject  = 'Reset Your Password'
            template = 'user_account/reset_password_verification.html'
            try:
              send_link(request, user, subject, template)
            except Exception as e:
              return Response({"error": f"Email could not be sent: {str(e)}"}, status=500)

            return Response({"message": "To reset your password.Please click on the link sent to your registered email"},status=status.HTTP_200_OK)

class ConfirmResetPassword(APIView):
      authentication_classes = []
      permission_classes = [AllowAny]
      def post(self,request,uidb64,token):
            password = request.data.get('password')
            confirm_password = request.data.get('confirm_password')
            if password is None or confirm_password is None:
                  return Response({'message':'please provide both the passwords'},status=status.HTTP_400_BAD_REQUEST)
            try:
                  uid = urlsafe_base64_decode(uidb64).decode()
                  user = CustomUser.objects.get(id=uid)
            except  (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
                  return Response({'message':"Invaid or expired Token"},status=status.HTTP_401_UNAUTHORIZED)
            if user is not None and  default_token_generator.check_token(user,token):
                  if password != confirm_password:
                        return Response({'message':"passwords must match"},status=status.HTTP_400_BAD_REQUEST)
                  try:
                        validate_password(password)
                  except ValidationError as e:
                        return Response({'error':list(e.messages)},status=status.HTTP_400_BAD_REQUEST) 
                  user.set_password(password)
                  user.save()
                  return Response({'message':'Password reset successfull!'},status=status.HTTP_201_CREATED)
            return Response({'message':"Invaid or expired Token"},status=status.HTTP_401_UNAUTHORIZED)
      


                  

            


      


class ProfileView(APIView):
      authentication_classes = [CustomAuthentication]
      Permission_classes = [IsAuthenticated]
      def get(self,request):
          return Response({
                'name':request.user.get_full_name(),
                'email':request.user.email

          })     
            

            
