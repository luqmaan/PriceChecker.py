from pychecker import configuration
from twilio.rest import TwilioRestClient
from twilio import twiml


account = configuration.account
token = configuration.token
from_ = configuration.from_
client = TwilioRestClient(account, token)


def notify(user, product, new_price):
    message = "Hello " + str(user.username) + " . The price of " + str(product.name) + " has changed to " + str(new_price)

    client.calls.create(to=user.phone,
                        from_=from_,
                        url="http://icmps.org:8888/call/" + str(user.id) +
                        "/" + str(product.id) + "/" + str(new_price))

    client.sms.messages.create(to=user.phone,
                               from_=from_,
                               body=message)
