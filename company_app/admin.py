from django.contrib import admin
from .models import *
from django.apps import apps

# apps = apps.get_app_config('company_app')

# for model_name, model in apps.models.items():
#     admin.site.register(model)

class FileManagerAdmin(admin.ModelAdmin):
    list_display = ['id','folder_name' ,'is_active','upload']
    search_fields = ['folder_name']
    list_filter = ['folder_name']

admin.site.register(FileManager, FileManagerAdmin)

class ManagerServicesAdmin(admin.ModelAdmin):
    list_display = ['id','tittle' ,'paid_amount','manager','is_active']

admin.site.register(ManagerServices, ManagerServicesAdmin)


class ServicesRequestsAdmin(admin.ModelAdmin):
    list_display = ['id','tittle' ,'paid_amount','request_user','approval_user','transaction_id','manager_service']

admin.site.register(ServicesRequests, ServicesRequestsAdmin)


class NotificationsAdmin(admin.ModelAdmin):
    list_display = ['id','tittle' ,'user']

admin.site.register(Notifications, NotificationsAdmin)