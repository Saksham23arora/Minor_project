import os
from twilio.rest import Client
from credentials import *

def send_sms(amount:str):

    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    #account_sid = os.environ['TWILIO_ACCOUNT_SID']
    #auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            body=f'Dear Customer , Your Bill amount of Rupees {amount} is due for Electricity bill . Please visit our site to pay it. Last date for payment is 31/12/21.',
            from_='+12395796344',
            to='+917696046760'
        )

    print(message.sid)

if __name__ == '__main__':
    send_sms('566')