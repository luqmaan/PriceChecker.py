#Twilio

from twilio.rest import TwilioRestClient

client = TwilioRestClient()

def TwilioMsg():
    client.sms.messages.create(to="", from_="",body="Hello there!")
    
def TwilioCall():
    client.calls.create(to="",from_="",url="http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient")
    
TwilioMsg()
TwilioCall()
