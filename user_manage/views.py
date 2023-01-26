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
from company_app.functions import get_files_dict,get_files_id_check,get_files_folder_dict,folder_files_name_update,get_files_folder_dict_list,get_files_info

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
            user_obj = LoginUser.objects.filter(Q(email=user_name) | Q(phone_number=user_name)).first()
            profile_pic = get_files_info(user_obj.picture)
            if not user_obj:
                return Response({"status":"400","message":"Please enter a valid number."})

            if user_obj and user_obj.is_active == False or user_obj and user_obj.is_manager == False and user_obj.is_company == False:
                return Response({"status":"400","message":"You are not a active user."})
            
            if "otp" in post_data:
                auth_check = UserAuthKey()
                if auth_check.validate_key(user_name,post_data['otp']):
                    token, _ = Token.objects.get_or_create(user=user_obj)
                    extra_values = {}
                    if user_obj.is_company:
                        manager_obj = ManagerCompany.objects.filter(company=user_obj).first()
                        if not manager_obj.manager.is_active:
                            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Cant login now. manager inactive stage."})

                        manager = manager_obj.manager
                        extra_values.update({"manager_data":{
                            'first_name':manager.first_name,
                            'last_name':manager.last_name,
                            'phone_number':str(manager.phone_number),
                        }})
                    else:
                        extra_values.update({"manager_data":{}})
                    expiry_date_obj = user_obj.expiry_date
                    expiry_date_str = str(expiry_date_obj) if expiry_date_obj else ""
                    expiry_date = ""
                    if expiry_date_obj:
                        expiry_date = expiry_date_obj.strftime("%Y-%m-%d %H:%M:%S")
                    return Response({"status":status.HTTP_201_CREATED,"message":"Login Successfull.","data":{
                        "token":token.key,
                        "first_name":user_obj.first_name,
                        "last_name":user_obj.last_name,
                        "phone_code":user_obj.phone_code,
                        "phone_number":str(user_obj.phone_number),
                        "email":user_obj.email,
                        "company":user_obj.is_company,
                        "manager":user_obj.is_manager,
                        "active":user_obj.is_active,
                        "expiry_date_value":expiry_date_str,
                        "expiry_date":expiry_date,
                        "profile_pic":profile_pic,
                        **extra_values
                    }})
                else:
                    return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please enter a valid OTP."})
                
            else:
                auth_key = UserAuthKey()
                auth_key.generate_token(user_name)
                return Response({"status":status.HTTP_201_CREATED,"message":"OTP send succcessfully.","data":auth_key.code})
            
            
        except Exception as e:
            traceback.print_exc()
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":str(e)})

class AdminAccountLogin(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        try:
            post_data = request.data
            if "user_name" not in post_data:
                return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"User name key missing."})
            
            if "password" not in post_data:
                return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Password missing."})

            user_name = post_data['user_name']
            password = post_data['password']
            user_obj = LoginUser.objects.filter(Q(email=user_name)  | Q(phone_number=user_name)).first()
            if user_obj and user_obj.is_active == False or user_obj and user_obj.is_admin == False:
                return Response({"status":"400","message":"You are not a active user or admin user."})
            
            if user_obj and user_obj.check_password(password):
                auth_check = UserAuthKey()
                
                token, created = Token.objects.get_or_create(user=user_obj)
                return Response({"status":status.HTTP_201_CREATED,"message":"Login Successfull.","data":{
                    "token":token.key,
                    "first_name":user_obj.first_name,
                    "last_name":user_obj.last_name,
                    "phone_code":user_obj.phone_code,
                    "phone_number":str(user_obj.phone_number),
                    "email":user_obj.email,
                }})
                
            else:
                return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please enter valid password."})
            
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
            user_obj.username = post_data['phone']
            user_obj.first_name = post_data['name']
            user_obj.last_name = post_data['company_name']
            user_obj.email = post_data['email']
            user_obj.phone_number = post_data['phone']
            user_obj.password = post_data['phone']
            user_obj.is_manager = True
            user_obj.save()
            return Response({"status":200,"message":"Manager Create Successfull."})
            
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

            post_data = request.data
            user_obj = request.user
            if not user_obj:
                return Response({"status":400,"message":"Not a valid manager."})

            user_obj_exist = LoginUser.objects.filter(Q(phone_number=post_data['phone']) | Q(email=post_data['email'])).first()
            if user_obj_exist:
                return Response({"status":400,"message":"Phone number or email already registerd."})
            
            company_obj = LoginUser()
            company_obj.first_name = post_data['name'] if 'name' in post_data else ""
            company_obj.last_name = post_data['company_name']
            company_obj.email = post_data['email'] if 'email' in post_data else ""
            company_obj.phone_number = post_data['phone']
            company_obj.is_manager = False
            company_obj.is_company = True
            company_obj.is_active = True
            company_obj.save()

            mapper = ManagerCompany()
            mapper.manager = user_obj
            mapper.company = company_obj
            mapper.company_name = post_data['company_name']
            mapper.save()

            return Response({"status":200,"message":"Account Created."})
        except:
            # traceback.print_exc()
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please try again latter."})
    
    def delete(self, request, *args, **kwargs):
        try:
            user_obj = request.user
            post_data = request.data
            company_id = post_data["company_id"] if "company_id" in post_data else None
            if company_id:
                company = ManagerCompany.objects.filter(manager=user_obj,id=company_id).first()
                company.is_delete = True
                company.is_active = False
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
            return Response({"status":200,"message":"Company List.",'data':res_data.data})
        except:
            # traceback.print_exc()
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please try again latter."})

class AdminManagerList(generics.ListCreateAPIView):
    queryset = LoginUser.objects.all()
    serializer_class = LoginUserSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            status = self.request.query_params.get('status',None)
            if request.user.is_admin:
                self.queryset = self.queryset.filter(is_manager=True)
                if status == "expired":
                    self.queryset = self.queryset.filter(is_active=False)
                else:
                    self.queryset = self.queryset.filter(is_active=True)
            else:
                self.queryset = LoginUser.objects.none()
            res_data = super().get(self, request, *args, **kwargs)
            return Response({"status":200,"message":"Manager List.",'data':res_data.data})
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
                self.queryset = self.queryset.filter(manager=request.user,is_active=True)
            else:
                self.queryset = LoginUser.objects.none()

            res_data = super().get(self, request, *args, **kwargs)
            return Response({"status":200,"message":"Company list.",'data':res_data.data})
        except:
            traceback.print_exc()
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please try again latter."})

class CreateEmployee(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        try:

            post_data = request.data
            user_obj = request.user
            if not request.user.is_company:
                return Response({"status":400,"message":"You cant create employees."})
            
            company_obj = EmployeeDetails()
            company_obj.company = user_obj
            company_obj.code = post_data['code']
            company_obj.f_name = post_data['f_name']
            company_obj.l_name = post_data['l_name']
            company_obj.description = post_data['description']
            company_obj.documents = post_data['documents'] if "documents" in post_data else []
            company_obj.save()

            return Response({"status":200,"message":"Account Created."})
        except:
            traceback.print_exc()
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please try again latter."})
    
    def delete(self, request, *args, **kwargs):
        try:
            user_obj = request.user
            post_data = request.data
            if not request.user.is_company:
                return Response({"status":400,"message":"You cant create employees."})

            employee_id = post_data["employee_id"] if "employee_id" in post_data else None
            if employee_id:
                company = EmployeeDetails.objects.filter(company=user_obj,id=employee_id).first()
                company.is_delete = True
                company.is_active = False
                company.save()
        except:
            traceback.print_exc()
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please try again latter."})

class EmployeeList(generics.ListCreateAPIView):
    queryset = EmployeeDetails.objects.all()
    serializer_class = EmployeeDetailsSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            if request.user.is_company:
                self.queryset = self.queryset.filter(company=request.user,is_active=True)
            elif request.user.is_manager:
                company = self.request.query_params.get('company',None)
                if company:
                    self.queryset = self.queryset.filter(company__id__in=list(ManagerCompany.objects.filter(manager=request.user,company__id=company).values_list('company',flat=True).all()),is_active=True)
                else:
                    self.queryset = self.queryset.filter(company__id__in=list(ManagerCompany.objects.filter(manager=request.user).values_list('company',flat=True).all()),is_active=True)
                
            else:
                self.queryset = EmployeeDetails.objects.none()

            res_data = super().get(self, request, *args, **kwargs)
            return Response({"status":200,"message":"Employee list.",'data':res_data.data})
        except:
            # traceback.print_exc()
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please try again latter."})

class AccountDocumentUpload(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            result_dict = {}
            user_obj = request.user
            if user_obj.is_company or user_obj.is_manager:
                documents_list = user_obj.documents
                result_dict = get_files_folder_dict_list(documents_list)
            
            return Response({"status":200,"message":"Document List.","data":result_dict})
        except:
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please try again latter."})
    
    def post(self, request, *args, **kwargs):
        try:
            user_obj = request.user
            request_post = request.data
            if user_obj.is_company or user_obj.is_manager and 'document' in request_post:
                documents_list = user_obj.documents if type(user_obj.documents) == list else []
                new_documents_list = get_files_id_check(request_post['document'])
                
                folder_name = request_post['folder_name'] if 'folder_name' in request_post else "default"
                folder_files_name_update(request_post['document'],folder_name)

                documents_list += new_documents_list
                request.user.documents = documents_list
                request.user.save()
                return Response({"status":200,"message":"Document updated."})
                    
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Not a valid user."})
        except:
            traceback.print_exc()
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please try again latter."})

class EmployeeDocumentUpload(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request,emp_id, *args, **kwargs):
        try:
            documents_list = []
            result_dict = {}
            user_obj = request.user
            emp_obj = EmployeeDetails.objects.filter(id=emp_id,is_active=True,is_delete=False)
            if user_obj.is_company:
                emp_obj = emp_obj.filter(company=user_obj).first()
                if emp_obj:
                    documents_list = emp_obj.documents
                
                else:
                    return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Not a valid employee.","data":result_dict})

            elif user_obj.is_manager:
                company = self.request.query_params.get('company',None)
                if company:
                    emp_obj = emp_obj.filter(company__id__in=list(ManagerCompany.objects.filter(manager=user_obj,company__id=company).all())).first()
                else:
                    emp_obj = emp_obj.filter(company__id__in=list(ManagerCompany.objects.filter(manager=user_obj).all())).first()

                if emp_obj:
                    documents_list = emp_obj.documents
            
            if documents_list:
                result_dict = get_files_folder_dict_list(documents_list)

            return Response({"status":200,"message":"Document List.","data":result_dict})
        except:
            traceback.print_exc()
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please try again latter."})
    
    def post(self, request,emp_id, *args, **kwargs):
        try:
            emp_obj = EmployeeDetails.objects.filter(id=emp_id,is_active=True,is_delete=False)
            user_obj = request.user
            request_post = request.data
            if user_obj.is_company and 'document' in request_post:
                folder_name = request_post['folder_name'] if 'folder_name' in request_post else "default"
                new_documents_list = get_files_id_check(request_post['document'])
                folder_files_name_update(request_post['document'],folder_name)
                emp_obj = emp_obj.filter(company=user_obj).first()
                if emp_obj:
                    documents_list = emp_obj.documents if type(emp_obj.documents) == list else []
                    emp_obj.documents = documents_list + new_documents_list
                    emp_obj.save()
                
                return Response({"status":200,"message":"Document updated."})
                    
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Not a valid employee id."})
        except:
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please try again latter."})


class CompanyDocuments(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request,company_id, *args, **kwargs):
        try:
            result_dict = []
            documents_list = []
            user_obj = request.user
            exist = ManagerCompany.objects.filter(company__id=company_id,manager=user_obj).first()
            if exist and user_obj.is_manager:
                
                if exist.company:
                    documents_list = exist.company.documents
                else:
                    return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Not a valid company.","data":result_dict})
            if documents_list:
                result_dict = get_files_folder_dict_list(documents_list)
            return Response({"status":200,"message":"Document List.","data":result_dict})
        except:
            traceback.print_exc()
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please try again latter."})
    
    def post(self, request,company_id, *args, **kwargs):
        try:
            user_obj = request.user
            request_post = request.data
            if user_obj.is_manager and 'document' in request_post:
                exist = ManagerCompany.objects.filter(company__id=company_id,manager=user_obj).first()
                if exist:
                    company_obj = LoginUser.objects.filter(id=company_id).first()
                    if company_obj:
                        documents_list = company_obj.documents if type(company_obj.documents) == list else []
                        new_documents_list = get_files_id_check(request_post['document'])
                        folder_name = request_post['folder_name'] if 'folder_name' in request_post else "default"
                        folder_files_name_update(request_post['document'],folder_name)
                        documents_list += new_documents_list
                        company_obj.documents = documents_list
                        company_obj.save()
                        return Response({"status":200,"message":"Document updated."})
                    
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Not a valid user."})
        except Exception as e:
            # traceback.print_exc()
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":str(e)})


class UpdateDataProfile(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            user_obj = request.user
            user_values = LoginUser.objects.filter(id=user_obj.id).values().first()
            profile_image_id = user_values['picture'] if 'picture' in user_values and user_values['picture'] else ""
            user_values["profile_pic"] = get_files_info(profile_image_id)
            user_values["phone_number"] = str(user_values["phone_number"])
            return Response({"status":200,"message":"Account updated.","data":dict(user_values)})
        except:
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please try again latter."})


    def post(self, request, *args, **kwargs):
        try:
            user_obj = request.user
            request_data = request.data
            if 'first_name' in request_data and request_data['first_name']:
                user_obj.first_name = request_data['first_name']
            
            if 'last_name' in request_data and request_data['last_name']:
                user_obj.last_name = request_data['last_name']
            
            if 'phone_number' in request_data and request_data['phone_number']:
                user_obj.phone_number = request_data['phone_number']
            
            if 'email' in request_data and request_data['email']:
                user_obj.email = request_data['email']

            if 'picture' in request_data and request_data['picture']:
                user_obj.picture = request_data['picture']

            user_obj.save()
            return Response({"status":200,"message":"Account updated."})
        except:
            # traceback.print_exc()
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please try again latter."})

# class UpdateDataProfilePic(generics):
#     permission_classes = [IsAuthenticated]
#     def post(self, request, *args, **kwargs):
#         try:
#             pass
#             return Response({"status":200,"message":"Account updated."})
#         except:
#             # traceback.print_exc()
#             return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please try again latter."})


# from django.core.urlresolvers import reverse
# from admin_tools.menu import items, Menu

from admin_tools.menu.items import MenuItem

class HistoryMenuItem(MenuItem):
    title = 'History'

    def init_with_context(self, context):
        request = context['request']
        # we use sessions to store the visited pages stack
        history = request.session.get('history', [])
        for item in history:
            self.children.append(MenuItem(
                title=item['title'],
                url=item['url']
            ))
        # add the current page to the history
        history.insert(0, {
            'title': context['title'],
            'url': request.META['PATH_INFO']
        })
        if len(history) > 10:
            history = history[:10]
        request.session['history'] = history