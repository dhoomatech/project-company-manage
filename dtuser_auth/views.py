from django.shortcuts import render

from django.conf import settings
import traceback
from django.core.mail import send_mail
# Create your views here.

# TWILIO_ACCOUNT_SID = 'AC48fe8f20b2328ba4076368794fe7c766'
# TWILIO_AUTH_TOKEN = '8dc3d65247ebc9dbfdd4dd23bad33741'

def sms_twilio_send():

    # Download the helper library from https://www.twilio.com/docs/python/install
    import os
    from twilio.rest import Client

    # Find your Account SID and Auth Token in Account Info and set the environment variables.
    # See http://twil.io/secure
    # account_sid = "ACf5fee4714f7a25f1b15c419cc544e958"
    # auth_token = "c249c9dd51b396de064216e23a4f3e4b"
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        # client = Client(account_sid, auth_token)
        message = client.messages.create(
            body='Hi vishnu',
            from_='+13855263363',
            to='+919633752456'
            # to='+918943788706'
        )
        print(message.sid)

        # incoming_phone_number = client.incoming_phone_numbers.create(phone_number='9446458004')
        # print(incoming_phone_number.sid)
    
    except:
        traceback.print_exc()



def email_send(email,otp,name = "user"):
    subject = 'Login Verification Code.'
    message = f'Dear {name},\n We received a request to log in to your account. To complete the login process, please enter the following code on the website:OTP: {otp}'

    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email,]    
    send_mail( subject, message, email_from, recipient_list )


def email_notify_send(email_list,tittle,text):
    subject = tittle + ' Expiration Reminder.'
    message = f'Dear valued customer! ,\n {text}'

    email_from = settings.EMAIL_HOST_USER
    recipient_list = email_list
    send_mail( subject, message, email_from, recipient_list )

def welcome_mail(to_mail):

    from django.core.mail import EmailMultiAlternatives
    email_from = settings.EMAIL_HOST_USER
    subject, from_email, to = 'Welcome mail.', email_from, to_mail

    text_content = 'Welcome to Malfati.'
    html_content = "<h1>Hi Welcome to Malfati !!</h1><p>We're so happy you're here! The concept is simple. Malfati helps you get organized and get more done with your business.</p><p>Thanks,<br>The Malfati Team</p>"
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def request_mail(to_mail,user_mail):

    from django.core.mail import EmailMultiAlternatives
    email_from = settings.EMAIL_HOST_USER
    subject, from_email, to = 'Service request.', email_from, to_mail

    text_content = 'Ownerd PRO,'
    html_content = f"<h3>Hi PRO </h3><p>New service requested by {user_mail}. please check your application.</p><p>Thanks,<br>The Malfati Team</p>"
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def request_approve_mail(to_mail):

    from django.core.mail import EmailMultiAlternatives
    email_from = settings.EMAIL_HOST_USER
    subject, from_email, to = 'Service request approval.', email_from, to_mail

    text_content = 'Hi Company.'
    html_content = "<h3>Hi Company</h3><p>Your requst was approved.</p><p>Thanks,<br>The Malfati Team</p>"
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

