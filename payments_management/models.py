from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.postgres.fields import JSONField

# Create your models here.


STATUS = [
    ('pending', 'Payment Pending'),
    ('paid', 'Payment Paid'),
    ('cancelled', 'Payment Cancelled'),
    ('hold', 'Payment Hold'),
]

class Transactions(models.Model):
    tittle = models.CharField(max_length=250, blank=False, null=True)
    paid_amount = models.CharField(max_length=250, blank=False, null=True)
    currency = models.CharField(max_length=150, blank=False, null=True)
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='from_user',blank=True,null=True)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='to_user',blank=True,null=True)
    request_type = models.CharField(max_length=150, blank=False, null=True)
    discription = models.TextField(blank=False, null=True)
    status = models.CharField(max_length=250, blank=False, null=True,choices=STATUS,default="initiated")
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True)
    transaction_id = models.CharField(max_length=250, blank=False, null=True)

class MembershipPack(models.Model):
    tittle = models.CharField(max_length=250, blank=False, null=True)
    discription = models.TextField(blank=False, null=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)
    amount = models.FloatField(blank=False, null=True,default=0.0)

class userCardData(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='card_user',blank=True,null=True)
    token = models.CharField(max_length=250, blank=False, null=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    payment_data = models.JSONField(null=True, blank=True)

class SubscriptionList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sub_user',blank=True,null=True)
    package = models.ForeignKey(MembershipPack, on_delete=models.CASCADE, related_name='user_package',blank=True,null=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    try_count = models.IntegerField(default=True,blank=False, null=True)
    