from django.shortcuts import render
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from account import serializers
from account.models import User
from rest_framework import status
from django.contrib.auth import authenticate
from account.serializers import UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer,UserPasswordChangeSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.

#create token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



class UserRegistration(APIView):
    def post(self,request):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token=get_tokens_for_user(user)
            return Response({"token":token,"msg":"Registration successfully..!!"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,staus=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    def post(self,request):
        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            em=serializer.data.get("email")
            pas=serializer.data.get("password")
            user=authenticate(email=em,password=pas)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({"token":token,"msg":"logged in successfully...!!"},status=status.HTTP_200_OK)
            else:
                return Response({"errors":{"non_field_errors":['Email or Password is not valid..!!']}},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


        
class UserProfile(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        serializer=UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)


class UserPasswordChange(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer=UserPasswordChangeSerializer(data=request.data,context={"user":request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({"msg":"Password changed successfully..!!"},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class UserLogout(APIView):
    def post(self, request, format=None):
        try:
            refresh_token = request.data.get('refresh_token')
            token_obj = RefreshToken(refresh_token)
            print(token_obj)
            token_obj.blacklist()
            return Response({"msg":"logout successfully...!!"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)



# class SendPasswordResetEmailView(APIView):
#     permission_classes=[IsAuthenticated]
#     def post(self,request):
#         serializer= SendPasswordResetEmailSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             return Response({"msg":"Password Reset link send. Please check your Email"},status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# class SavePasswordResetEmailView(APIView):
#     def post(self,request,uid,token):
#         serializer=UserPasswordResetEmailSerializer(data=request.data,context={"uid":uid,'token':token})
#         if serializer.is_valid(raise_exception=True):
#             return Response({"msg":"Password Reset Successfully..!!"})
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)