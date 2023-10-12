from calendar import c
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "company_management.settings")
django.setup()



from dtuser_auth.views import sms_twilio_send,email_send,welcome_mail,request_mail,request_approve_mail

to_mail = "nishad@gmail.com"
welcome_mail(to_mail)

# email_send("nishadgolapakrishnan0@dhoomatech.com","23456")

# sms_twilio_send()

# from user_manage.models import LoginUser

