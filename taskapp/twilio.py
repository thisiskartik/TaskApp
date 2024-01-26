import os
from twilio.rest import Client

client = Client(os.environ.get('TWILIO_ACCOUNT_SID'),
                os.environ.get('TWILIO_AUTH_TOKEN'))


def send_sms(body, to):
    client.messages.create(from_=os.environ.get('TWILIO_FROM_PHONE_NUMBER'),
                           to=to, body=body)


def call(url, to):
    client.calls.create(from_=os.environ.get('TWILIO_FROM_PHONE_NUMBER'),
                        to=to, url=url)
