from google.appengine.ext import webapp
from google.appengine.api import mail
from google.appengine.ext.webapp.util import run_wsgi_app

class CronMailer(webapp.RequestHandler):
    def get(self):
        message = mail.EmailMessage(sender="From Email Address",subject="Hello")
        message.to = "To Email Address"
        message.body = "Hai"
        message.send()

application = webapp.WSGIApplication([('/', CronMailer)],debug=True)
def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
