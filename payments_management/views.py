from django.shortcuts import redirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
import traceback
from .models import *
from .serializers import TransactionSerializer

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

class TransactionList(generics.ListCreateAPIView):
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