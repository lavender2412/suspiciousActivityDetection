
# importing twilio
from twilio.rest import Client

def sendsms():  
    # Your Account Sid and Auth Token from twilio.com / console
    account_sid = 'YOUR_ACCOUNT_SID'
    auth_token = 'AUTH_TOKEN'
    
    client = Client(account_sid, auth_token)
    
    ''' Change the value of 'from' with the number 
    received from Twilio and the value of 'to'
    with the number in which you want to send message.'''
    message = client.messages.create(
                                from_='+16205221571',
                                body ='Suspicious Alert! Please look into it. ',
                                to ='+9191217169826'
                            )
    print(message.sid)

