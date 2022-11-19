import traceback
from rest_framework.response import Response 
from rest_framework.views import APIView
from django.utils.translation import gettext as _
from rest_framework import status
from django.core.mail import send_mail as sm
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import generics
from django.conf import settings

from .models import FileManager,ServicesRequests
from .serializers import *
from user_manage.models import ManagerCompany,LoginUser
# Create your views here.


from django.core.files.base import ContentFile
import base64
import random
import string


class FileUploadBase64(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        try:
            datalist = {}
            data = request.data
            if 'image_encode' in data and data['image_encode']:
                file = data['image_encode']
                file_exe = data['image_type'] if "image_type" in data else "png"
                output_string = ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(10))
                imgname = output_string + "." + file_exe
                your_file = ContentFile(base64.b64decode(file),imgname)
                f = FileManager.objects.create(upload=your_file)
                datalist.update({"image":f.pk})
                return Response({
                    'status':"success",
                    'message': 'Image added successfully',
                    'response_code': status.HTTP_200_OK,
                    'data':datalist
                })
            return Response({
                    'status':"success",
                    'message': 'Image not added. Please check post data.',
                    'response_code': status.HTTP_200_OK,
                    'data':datalist
                })
        except Exception as e:
            message = str(e)     
            return Response({'status':'error','response_code':500,"message":message})


class ServicesRequestsCreate(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        try:
            user_obj = request.user
            post_data = request.data
            if user_obj.is_company:
                report_obj = ManagerCompany.objects.filter(company=user_obj).first()
                report_user = report_obj.manager
                request_type = 'company_request'
                pass
            if user_obj.is_manager:
                request_type = 'manager_request'
                report_user = LoginUser.objects.filter(id=settings.ADMIN_USER_ID).first()
                pass
            if report_user:
                service_obj = ServicesRequests()
                service_obj['tittle'] = post_data['tittle']
                service_obj['paid_amount'] = post_data['paid_amount'] if 'paid_amount' in post_data else ''
                service_obj['discription'] = post_data['discription'] if 'discription' in post_data else ''
                service_obj['documents'] = post_data['documents'] if 'documents' in post_data else ''
                service_obj['approval_user'] = report_user
                service_obj['request_user'] = user_obj
                service_obj['request_type'] = request_type
                service_obj.save()

                return Response({
                    'status':"success",
                    'message': 'Request created successfull.',
                    'response_code': status.HTTP_200_OK,
                })
            else:
                return Response({
                    'status':"failed",
                    'message': "You can't process now.",
                    'response_code': 400,
                })

        except Exception as e:
            message = str(e)     
            return Response({'status':'error','response_code':500,"message":message})

    def key_exist_check(fields = {},keys=[],null_check=True):
        if keys:
            non_keys = [key for key in keys if (key not in fields) or (key in fields and not fields[key] and null_check)]
            if non_keys:
                message = "Required Key Missing!. ( "
                message += ",".join(non_keys)
                message += " )"
                return message

        return False


class ServicesRequestsApproval(generics.ListCreateAPIView):
    queryset = ServicesRequests.objects.all()
    serializer_class = ServicesRequestsSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            user_obj = request.user
            self.queryset = self.queryset.filter(approval_user=user_obj)
            res_data = super().get(self, request, *args, **kwargs)
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Service request list.",'data':res_data.data})
        except:
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please try again latter."})


class MyServicesRequests(generics.ListCreateAPIView):
    queryset = ServicesRequests.objects.all()
    serializer_class = ServicesRequestsSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            user_obj = request.user
            self.queryset = self.queryset.filter(request_user=user_obj)
            res_data = super().get(self, request, *args, **kwargs)
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Service request list.",'data':res_data.data})
        except:
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please try again latter."})