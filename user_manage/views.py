import traceback
from django.shortcuts import render

# Create your views here.
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import generics
from .serializers import *

from django.db.models import Q
from dtuser_auth.models import UserAuthKey
from .models import LoginUser,ManagerCompany

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class AccountLogin(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        try:
            post_data = request.data
            if "user_name" not in post_data:
                return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"User name key missing."})
            
            user_name = post_data['user_name']
            user_obj = LoginUser.objects.filter(Q(email=user_name) | Q(username=user_name) | Q(phone_number=user_name)).first()
            if user_obj and user_obj.is_active == False or user_obj.is_manager == False and user_obj.is_company == False:
                return Response({"status":"400","message":"You are not a active user."})
            
            if "otp" in post_data:
                auth_check = UserAuthKey()
                if auth_check.validate_key(user_name):
                    token, created = Token.objects.get_or_create(user=user_obj)
                    return Response({"status":status.HTTP_201_CREATED,"message":"Login Successfull.","data":{
                        "token":token,
                        "first_name":user_obj.first_name,
                        "last_name":user_obj.last_name,
                        "phone_code":user_obj.phone_code,
                        "phone_number":user_obj.phone_number,
                        "email":user_obj.email,
                        "company":user_obj.is_company,
                        "manager":user_obj.is_manager,
                    }})
                
            else:
                auth_key = UserAuthKey()
                auth_key.generate_token(user_name)
                return Response({"status":status.HTTP_201_CREATED,"message":"OTP succcessfully send.","data":auth_key.code})
            
        except Exception as e:
            # traceback.print_exc()
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":str(e)})

class AdminAccountLogin(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        try:
            post_data = request.data
            if "user_name" not in post_data:
                return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"User name key missing."})
            
            user_name = post_data['user_name']
            user_obj = LoginUser.objects.filter(Q(email=user_name) | Q(username=user_name) | Q(phone_number=user_name)).first()
            if user_obj and user_obj.is_active == False or user_obj and user_obj.is_admin == False:
                return Response({"status":"400","message":"You are not a active user."})
            
            if "otp" in post_data:
                auth_check = UserAuthKey()
                if auth_check.validate_key(user_name):
                    token, created = Token.objects.get_or_create(user=user_obj)
                    return Response({"status":status.HTTP_201_CREATED,"message":"Login Successfull.","data":{
                        "token":token,
                        "first_name":user_obj.first_name,
                        "last_name":user_obj.last_name,
                        "phone_code":user_obj.phone_code,
                        "phone_number":user_obj.phone_number,
                        "email":user_obj.email,
                    }})
                
            else:
                auth_key = UserAuthKey()
                auth_key.generate_token(user_name)
                return Response({"status":status.HTTP_201_CREATED,"message":"OTP succcessfully send.","data":auth_key.code})
            
        except:
            traceback.print_exc()
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please try again latter."})

class CreateManagerAccount(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        try:
            post_data = request.data
            for key in ["name","company_name","email","phone"]:
                if key not in post_data:
                    return Response({"status":status.HTTP_400_BAD_REQUEST,"message":key+" Missing. Please add required keys"})
            
            user_obj = LoginUser()
            user_obj.first_name = post_data['name']
            user_obj.last_name = post_data['company_name']
            user_obj.email = post_data['email']
            user_obj.phone_number = post_data['phone']
            user_obj.is_manager = True
            user_obj.save()

        except Exception as e:
            traceback.print_exc()
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":str(e)})
    
    def check_mail(self,email):
        import re
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if(re.fullmatch(regex, email)):
            return True
    
        else:
            return False

class CreateCompanyAccount(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        try:
            user_obj = request.user
            post_data = request.data

            company_obj = LoginUser()
            company_obj.first_name = post_data['name'] if 'name' in post_data else ""
            company_obj.last_name = post_data['company_name']
            company_obj.email = post_data['email'] if 'email' in post_data else ""
            company_obj.phone_number = post_data['phone']
            company_obj.is_manager = False
            company_obj.is_company = True
            company_obj.save()

            mapper = ManagerCompany()
            mapper.manager = user_obj
            mapper.company = company_obj
            mapper.company_name = post_data['company_name']

        except:
            traceback.print_exc()
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please try again latter."})
    
    def delete(self, request, *args, **kwargs):
        try:
            user_obj = request.user
            post_data = request.data
            company_id = post_data["company_id"] if "company_id" in post_data else None
            if company_id:
                company = ManagerCompany.objects.filter(manager=user_obj,id=company_id).first()
                company.is_delete = True
                company.is_active = True
                company.save()
        except:
            traceback.print_exc()
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please try again latter."})


class AdminCompanyList(generics.ListCreateAPIView):
    queryset = LoginUser.objects.all()
    serializer_class = LoginUserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            if request.user.is_admin:
                self.queryset = self.queryset.filter(is_company=True)
            else:
                self.queryset = LoginUser.objects.none()
            res_data = super().get(self, request, *args, **kwargs)
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Company List.",'data':res_data.data})
        except:
            # traceback.print_exc()
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please try again latter."})

class AdminManagerList(generics.ListCreateAPIView):
    queryset = LoginUser.objects.all()
    serializer_class = LoginUserSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            if request.user.is_admin:
                self.queryset = self.queryset.filter(is_manager=True)
            else:
                self.queryset = LoginUser.objects.none()
            res_data = super().get(self, request, *args, **kwargs)
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Manager List.",'data':res_data.data})
        except:
            traceback.print_exc()
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please try again latter."})


class CompanyList(generics.ListCreateAPIView):
    queryset = ManagerCompany.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            if request.user.is_manager:
                self.queryset = self.queryset.filter(company=request.user,is_active=True)
            else:
                self.queryset = LoginUser.objects.none()
            res_data = super().get(self, request, *args, **kwargs)
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Company list.",'data':res_data.data})
        except:
            traceback.print_exc()
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please try again latter."})

