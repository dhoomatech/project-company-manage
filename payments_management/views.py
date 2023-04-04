from django.shortcuts import redirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from rest_framework import generics
from rest_framework.response import Response
import traceback
from .models import *
from .serializers import *
from django.http import JsonResponse  

from user_manage.models import LoginUser
from datetime import date, timedelta
from django.conf import settings

# import razorpay

# Create your views here.
# @api_view(['POST'])
# def createOrder(request):
#     global client
#     data = request.data

#     amount = int(float(data['amount']))

#     client = razorpay.Client(auth=("<key_id>", "<key_secret>"))

#     data = {"amount" : amount, "currency" : "INR"}
#     payment = client.order.create(data=data)

#     return Response({'order_id': payment['id'], 'amount': payment['amount'], 'currency':payment['currency']})

# @api_view(['POST'])
# def verifySignature(request):
#     res = request.data

#     params_dict = {
#         'razorpay_payment_id' : res['razorpay_paymentId'],
#         'razorpay_order_id' : res['razorpay_orderId'],
#         'razorpay_signature' : res['razorpay_signature']
#     }

#     # verifying the signature
#     res = client.utility.verify_payment_signature(params_dict)

#     if res == True:
#         return Response({'status':'Payment Successful'})
#     return Response({'status':'Payment Failed'})

class TransactionList(generics.ListAPIView):
    queryset = Transactions.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            if request.user:
                self.queryset = self.queryset.filter(to_user=request.user)
            else:
                self.queryset = Transactions.objects.none()
            res_data = super().get(self, request, *args, **kwargs)
            return Response({"status":200,"message":"Manager List.",'data':res_data.data})
        except:
            traceback.print_exc()
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please try again latter."})


class TransactionFromList(generics.ListCreateAPIView):
    queryset = Transactions.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            if request.user:
                self.queryset = self.queryset.filter(from_user=request.user)
            else:
                self.queryset = Transactions.objects.none()
            res_data = super().get(self, request, *args, **kwargs)
            return Response({"status":200,"message":"Manager List.",'data':res_data.data})
        except:
            traceback.print_exc()
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please try again latter."})

class MembershipPackage(generics.ListAPIView):
    queryset = MembershipPack.objects.all().filter(is_active=True)
    serializer_class = MembershipPackSerializer
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        try:
            res_data = super().get(self, request, *args, **kwargs)
            return Response({"status":200,"message":"Membership Package List.",'data':res_data.data})
        except:
            traceback.print_exc()
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please try again latter."})

class MembershipPackageAdmin(generics.ListCreateAPIView):
    queryset = MembershipPack.objects.all()
    serializer_class = MembershipPackSerializer
    permission_classes = [IsAdminUser]
    def get(self, request, *args, **kwargs):
        try:
            res_data = super().get(self, request, *args, **kwargs)
            return Response({"status":200,"message":"Membership Package List.",'data':res_data.data})
        except:
            traceback.print_exc()
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please try again latter."})

class MembershipPackageAdminUpdate(generics.RetrieveUpdateAPIView):
    queryset = MembershipPack.objects.all()
    serializer_class = MembershipPackSerializer
    permission_classes = [IsAdminUser]

# package_id=1&first_name=vishnu&middle_name=vp&last_name=calicut&email=vishnu@gmail.com&phone_code=91&phone_number=98989898989
class PaymentProcess(View):
    template_name = 'payments_management/payment_process.html'
    def get(self, request, *args, **kwargs):
        package_id = self.request.GET.get('package_id',None)
        first_name = self.request.GET.get('first_name')
        middle_name = self.request.GET.get('middle_name')
        last_name = self.request.GET.get('last_name')
        email = self.request.GET.get('email')
        phone_code = self.request.GET.get('phone_code')
        phone_number = self.request.GET.get('phone_number')
        amount = self.request.GET.get('amount')
        context = {
            "package_id":package_id,
            "first_name":first_name,
            "middle_name":middle_name,
            "last_name":last_name,
            "email":email,
            "phone_code":phone_code,
            "phone_number":phone_number,
            "package_amount":0.0,
            "package_name":"No Package",
            "amount_per_unit":"AED0",
            "total_amount":"AED0",
            "payment_key":settings.PAYMENT_KEY,
        }

        if package_id:
            package_obj = MembershipPack.objects.filter(id=package_id).first()
            if package_obj:
                if package_obj.amount > 0.0:
                    context.update({"package_name":package_obj.tittle,"package_amount":package_obj.amount,"amount_per_unit":"AED"+str(package_obj.amount),"total_amount":"AED"+str(package_obj.amount)})
                    return render(request, self.template_name,context)
                else:
                    user_obj = LoginUser.objects.filter(email=email).first()
                    if user_obj:
                        days_before = date.today() + timedelta(days=package_obj.expire_days)
                        user_obj.expiry_date = days_before
                        user_obj.is_active = True
                        user_obj.save()
                        return JsonResponse({"status":200,"message":"Free subscription added."})
                    else:
                        return JsonResponse({"status":400,"message":"Not a valid user."})
            else:
                return JsonResponse({"status":400,"message":"Package not found."})
            
        elif amount:
            amount_value = float(amount)
            context.update({"package_name":"Add fund","package_amount":amount_value,"amount_per_unit":"AED"+str(amount_value),"total_amount":"AED"+str(amount_value)})
            return render(request, self.template_name,context)

        return JsonResponse({"status":400,"message":"Payment can't process now."})


class PaymentProcess2(View):
    template_name = 'payments_management/payment_process.html'
    def get(self, request, *args, **kwargs):
        package_id = self.request.GET.get('package_id')
        first_name = self.request.GET.get('first_name')
        middle_name = self.request.GET.get('middle_name')
        last_name = self.request.GET.get('last_name')
        email = self.request.GET.get('email')
        phone_code = self.request.GET.get('phone_code')
        phone_number = self.request.GET.get('phone_number')
        context = {
            "package_id":package_id,
            "first_name":first_name,
            "middle_name":middle_name,
            "last_name":last_name,
            "email":email,
            "phone_code":phone_code,
            "phone_number":phone_number,
            "package_amount":0.0,
            "package_name":"No Package",
            "amount_per_unit":"AED0",
            "total_amount":"AED0",
            "redirect":True,
        }

        if package_id:
            package_obj = MembershipPack.objects.filter(id=package_id).first()
            if package_obj:
                context.update({"package_name":package_obj.tittle,"package_amount":package_obj.amount,"amount_per_unit":"AED"+str(package_obj.amount),"total_amount":"AED"+str(package_obj.amount)})
                print(context)
                return render(request, self.template_name,context)

        return JsonResponse({"status":400,"message":"Payment can't process now."})

class PaymentSucess(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        try:
            token = self.request.query_params.get('token',None)
            mode = self.request.query_params.get('mode',None)
            tap_id = self.request.query_params.get('tap_id',None)
            
            payment_obj = PaymentTransation.objects.filter(transaction_token=token).first()
            payment_obj.status = "paid"
            payment_obj.transaction_id = tap_id
            payment_obj.save()
            return Response({"status":200,"message":"Payment success."})
        except:
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please try again latter."})

class PaymentTokenUpdate(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        try:
            token = request.data['payment_token']
            mobile = request.data['phone']
            mode = request.data['mode'] if "mode" in request.data else ""
            PaymentTransation.objects.create(phone=mobile,transaction_token=token,paid_mode=mode)
            return Response({"status":200,"message":"Token update successfull."})
        except:
            traceback.print_exc()
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Please try again latter."})
            