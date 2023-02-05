from calendar import c
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "company_management.settings")
django.setup()

# importing date class from datetime module
from datetime import date

from user_manage.model import LoginUser

# creating the date object of today's date
todays_date = date.today()


LoginUser.objects.filter(expiry_date__lt=datetime.date(todays_date.year, todays_date.month, todays_date.day)).update(is_active=False)