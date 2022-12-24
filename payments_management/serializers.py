from rest_framework import serializers
from .models import *

from django.views.generic.base import View
from django.shortcuts import render


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ['id', 'tittle', 'paid_amount', 'currency','discription','status','created','modified']

class MembershipPackSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipPack
        fields = "__all__"

