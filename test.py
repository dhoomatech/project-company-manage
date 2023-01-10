from calendar import c
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "company_management.settings")
django.setup()

# from dtuser_auth.views import sms_twilio_send

# sms_twilio_send()

from user_manage.models import LoginUser

user_obj = LoginUser.objects.filter(email="vishnu@dhoomatech.com").first()
user_obj.is_staff = False
user_obj.phone_number = "+919633752456"
user_obj.is_superuser = True
user_obj.save()
print(user_obj.__dict__)
print(str(user_obj.phone_number))