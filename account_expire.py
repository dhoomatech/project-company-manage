from calendar import c
import os
import django
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "company_management.settings")
django.setup()

# importing date class from datetime module
from datetime import date,timedelta

from user_manage.models import LoginUser

# creating the date object of today's date
todays_date = date.today()



import schedule
import datetime
import time
from dtuser_auth.views import email_notify_send

def account_expire_job():
    LoginUser.objects.filter(expiry_date__lt=datetime.date(todays_date.year, todays_date.month, todays_date.day)).update(is_active=False)

    number_days = settings.EXPIRE_DATE_REMINDER
    today = datetime.now()
    end_date = today + timedelta(days=number_days)

    emial_list = list(LoginUser.objects.filter(expiry_date__lt=datetime.date(end_date.year, end_date.month, end_date.day),is_active=True).values_list("email",flat=True).all())

    tittle = "Account expire "
    text = "This is a friendly reminder that your account with us will expire soon.To continue using our services, we kindly request that you renew your account before the expiration date."
    email_notify_send(emial_list,tittle)


schedule.every(10).minutes.do(account_expire_job)
schedule.every().hour.do(account_expire_job)
schedule.every().day.at("12:00").do(account_expire_job)

while 1:
    schedule.run_pending()
    time.sleep(1)