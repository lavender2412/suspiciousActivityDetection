
# importing twilio
from twilio.rest import Client

def sendsms():  
    # Your Account Sid and Auth Token from twilio.com / console
    account_sid = 'ACa5ef40f9cb08b23c8401bc9cedcf85ce'
    auth_token = 'e86be0ebe8b7e6f56c6b60b332b0672b'
    
    client = Client(account_sid, auth_token)
    
    ''' Change the value of 'from' with the number 
    received from Twilio and the value of 'to'
    with the number in which you want to send message.'''
    message = client.messages.create(
                                from_='+16205221571',
                                body ='Suspicious Alert! Please look into it. ',
                                to ='+919121769826'
                            )
    print(message.sid)

