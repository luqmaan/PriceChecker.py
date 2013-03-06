#Email Notification

import smtplib

def SendEmail(toaddr,msg):
    fromaddr = 'PriceChecker12345@gmail.com'   

    username = 'PriceChecker12345@gmail.com'
    password = 'forpythonclass'

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddr, msg)
    server.quit()

toaddr='shano142@yahoo.com'
msg='Hellooooo'
SendEmail(toaddr,msg)



