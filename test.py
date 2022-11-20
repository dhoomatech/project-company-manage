from calendar import c
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "company_management.settings")
django.setup()

from dtuser_auth.views import sms_twilio_send

sms_twilio_send()