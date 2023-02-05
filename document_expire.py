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

FileManager.objects.filter(expiry_date__lte=ts).update(is_active=False)