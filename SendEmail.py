#Email Notification

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def SendEmail(to):
    msg = MIMEMultipart('alternative')

    msg['Subject'] = "Hello!"
    msg['From']    = "info@pychecker.com" 
    msg['To']      = to

    text = "Test message"
    part1 = MIMEText(text, 'plain')

    html = "<i>Hai this is a test email</i>"
    part2 = MIMEText(html, 'html')

    username = os.environ['MANDRILL_USERNAME']
    password = os.environ['MANDRILL_PASSWORD']

    msg.attach(part1)
    msg.attach(part2)

    s = smtplib.SMTP('smtp.mandrillapp.com', 25)
    s.login(username, password)

    s.sendmail(msg['From'], msg['To'], msg.as_string())

    s.quit()

toaddr = '' # To address
SendEmail(toaddr)



