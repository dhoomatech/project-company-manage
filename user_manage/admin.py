from django.contrib import admin
from .models import *
from django.apps import apps

apps = apps.get_app_config('user_manage')

admin.site.site_header = "Malfati Admin"
admin.site.site_title = "Malfati Admin Portal"
admin.site.index_title = "Welcome to Malfati Admin Portal"

# for model_name, model in apps.models.items():
#     admin.site.register(model)


@admin.action(description='Mark selected user approved')
def make_approved(modeladmin, request, queryset):
    queryset.update(is_active='t')

@admin.action(description='Mark selected user inactive')
def make_inactive(modeladmin, request, queryset):
    queryset.update(is_active='f')

class LoginUserAdmin(admin.ModelAdmin):
    list_display = ['id','phone_number' ,'first_name','last_name','created','is_manager','is_company','is_active']
    ordering = ['id']
    actions = [make_approved,make_inactive]

admin.site.register(LoginUser, LoginUserAdmin)