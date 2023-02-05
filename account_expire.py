from calendar import c
import os
import django
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "company_management.settings")
django.setup()

# importing date class from datetime module
from datetime import date

from user_manage.models import LoginUser

# creating the date object of today's date
todays_date = date.today()



import schedule
import time

def account_expire_job():
    LoginUser.objects.filter(expiry_date__lt=datetime.date(todays_date.year, todays_date.month, todays_date.day)).update(is_active=False)

    number_days = settings.EXPIRE_DATE_REMINDER
    today = datetime.now()
    end_date = today + timedelta(days=number_days)

    ts = datetime.timestamp(end_date)
    

schedule.every(10).minutes.do(account_expire_job)
schedule.every().hour.do(account_expire_job)
schedule.every().day.at("12:00").do(account_expire_job)

while 1:
    schedule.run_pending()
    time.sleep(1)