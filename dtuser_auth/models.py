from django.db import models
from django.db.models import Q
from django.utils import timezone
from user_manage.models import LoginUser
import random
import datetime
from twilio.rest import Client
from django.conf import settings
from django.core.mail import send_mail
# Create your models here.


class UserAuthKey(models.Model):
	code = models.CharField(max_length=100)
	user_name = models.CharField(max_length=250)
	date_time = models.DateTimeField(default=timezone.now)
	is_read = models.BooleanField(default=False)
	
	def generate_token(self,user_name,*args, **kwargs):
		UserAuthKey.objects.filter(user_name=user_name).delete()
		self.user_name = user_name
		self.code = random.randint(10000,99999)
		self.date = datetime.datetime.now() + datetime.timedelta(minutes=10)
		self.save()
		try:
			subject = 'Login Verification Code.'
			message = f'Dear Malfati user,\n We received a request to log in to your account. To complete the login process, please enter the following code on the website:OTP: {self.code}'

			email_from = settings.EMAIL_HOST_USER
			recipient_list = [user_name,]    
			send_mail( subject, message, email_from, recipient_list )

		except:
			import traceback
			traceback.print_exc()

			pass
	
	def validate_key(self,user_name,otp,*args, **kwargs):
		expire_time = timezone.now
		token_obj  = UserAuthKey.objects.filter(user_name=user_name,is_read=False,code=otp).first()
		if token_obj:
			# token_obj.is_read = True
			token_obj.save()
			# self.clean_expired_key()
			return True
		return False
	
	def clean_expired_key(self,*args, **kwargs):
		expire_time = timezone.now
		UserAuthKey.objects.filter(Q(date_time__gte=expire_time) | Q(is_read=True)).delete()