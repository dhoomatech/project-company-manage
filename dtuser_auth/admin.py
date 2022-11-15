from django.contrib import admin
from .models import *
from django.apps import apps

apps = apps.get_app_config('dtuser_auth')

for model_name, model in apps.models.items():
    admin.site.register(model)