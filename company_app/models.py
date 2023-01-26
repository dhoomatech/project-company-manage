from django.db import models
from django.utils import timezone
from django.conf import settings
# Create your models here.


STATUS = [
    ('approve', 'Approve'),
    ('decline', 'Decline'),
    ('initiated', 'Initiated'),
    ('hold', 'Hold'),
]

class FileManager(models.Model):
    folder_name = models.CharField(max_length=250, blank=False, null=True,default="default")
    user_code = models.CharField(max_length=50, blank=False, null=True)
    file_name = models.CharField(max_length=250, blank=False, null=True)
    upload = models.FileField(upload_to ='file_manager')
    is_active = models.BooleanField(default=True)
    expiry_date = models.DateField(blank=True, null=True)

class ManagerServices(models.Model):
    tittle = models.CharField(max_length=250, blank=False, null=True)
    paid_amount = models.CharField(max_length=250, blank=False, null=True)
    discription = models.TextField(blank=False, null=True)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='service_manager',blank=True,null=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True)
    documents = models.JSONField(default=dict,blank=True)
    
class ServicesRequests(models.Model):
    tittle = models.CharField(max_length=250, blank=False, null=True)
    paid_amount = models.CharField(max_length=250, blank=False, null=True)
    request_type = models.CharField(max_length=150, blank=False, null=True)
    discription = models.TextField(blank=False, null=True)
    request_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='request_user',blank=True,null=True)
    approval_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='approval_user',blank=True,null=True)
    status = models.CharField(max_length=250, blank=False, null=True,choices=STATUS,default="initiated")
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True)
    documents = models.JSONField(default=dict,blank=True)
    transaction_id = models.CharField(max_length=250, blank=False, null=True)
    manager_service = models.ForeignKey(ManagerServices, on_delete=models.CASCADE, related_name='approval_user',blank=True,null=True)


class Notifications(models.Model):
    tittle = models.CharField(max_length=250, blank=False, null=True)
    discription = models.TextField(blank=False, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user',blank=True,null=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True)