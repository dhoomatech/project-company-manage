from django.shortcuts import render

from django.conf import settings
# Create your views here.



def sms_twilio_send():
    from twilio.rest import Client
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                        from_='+12057547427',
                        to='+919633752456'
                    )

    print(message.sid)
