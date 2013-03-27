#Tweet

from twitter import *

def TweetFn(uName):
    token = ''
    token_secret = ''
    consumer = ''
    consumer_secret = ''
    t = Twitter(auth=OAuth(token,token_secret,consumer,consumer_secret)

    # Status Update
    #t.statuses.update(status = "Test Tweet Test")

    # Direct Message
    t.direct_messages.new(user=uName,text="Hello!")

username = "" # Enter username here
TweetFn(username)
