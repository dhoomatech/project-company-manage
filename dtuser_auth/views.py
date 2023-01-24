from django.shortcuts import render

from django.conf import settings
import traceback
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
            body='Hi there vishnu vp this message from dhoomatech.',
            from_='+13855263363',
            to='+919633752456'
            # to='+918943788706'
        )
        print(message.sid)

        # incoming_phone_number = client.incoming_phone_numbers.create(phone_number='9446458004')
        # print(incoming_phone_number.sid)
    
    except:
        traceback.print_exc()



    