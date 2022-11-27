from django.db import models
from django.utils import timezone
from django.conf import settings

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