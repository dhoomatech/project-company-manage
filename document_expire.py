from calendar import c
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "company_management.settings")
django.setup()


from company_app.models import FileManager

# using datetime module
import datetime;
# ct stores current time
ct = datetime.datetime.now()
# ts store timestamp of current time
ts = ct.timestamp()

import schedule
import time

def file_expire_job():
    FileManager.objects.filter(expiry_date__lte=ts).update(is_active=False)

schedule.every(10).minutes.do(file_expire_job)
schedule.every().hour.do(file_expire_job)
schedule.every().day.at("12:00").do(file_expire_job)

while 1:
    schedule.run_pending()
    time.sleep(1)
