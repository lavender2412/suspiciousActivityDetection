
# importing twilio
import os
from twilio.rest import Client
from dotenv import load_dotenv
load_dotenv()

def sendsms():  
    # Your Account Sid and Auth Token from twilio.com / console
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    from_number = os.getenv('TWILIO_FROM_NUMBER')
    to_number = os.getenv('TWILIO_TO_NUMBER')

    
    client = Client(account_sid, auth_token)
    
    ''' Change the value of 'from' with the number 
    received from Twilio and the value of 'to'
    with the number in which you want to send message.'''
    message = client.messages.create(
                                from_=from_number,
                                body ='Suspicious Alert! Please look into it. ',
                                to =to_number
                            )
    print(message.sid)

