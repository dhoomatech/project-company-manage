from django.shortcuts import render

from django.conf import settings
# Create your views here.

# TWILIO_ACCOUNT_SID = 'AC48fe8f20b2328ba4076368794fe7c766'
# TWILIO_AUTH_TOKEN = '8dc3d65247ebc9dbfdd4dd23bad33741'

def sms_twilio_send():

    # Download the helper library from https://www.twilio.com/docs/python/install
    import os
    from twilio.rest import Client

    # Find your Account SID and Auth Token in Account Info and set the environment variables.
    # See http://twil.io/secure
    account_sid = "AC710fde2a95d194182b74045bd8766186"
    auth_token = "7ac33a5dffce0630da84b50f826f2e3b"
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body='Hi there vishnu vp this message from dhoomatech.',
        from_='+16402237936',
        to='+919633752456'
        # to='+918943788706'
    )

    print(message.sid)

    