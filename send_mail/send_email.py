import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate

def main():

    msg = MIMEMultipart()
    msg['From']    = 'tim.f.vieira@gmail.com'
    msg['To']      = 'tim.f.vieira@gmail.com'
    msg['Date']    = formatdate(localtime=True)
    #msg['Date']    = 'Wed, 22 Jul 2019 22:37:56 -0500'
    msg['Subject'] = 'URGENT: Do *not* drink the coffee'
    msg.attach(MIMEText("""

Do *not* drink the coffee. It is POISONED.

"""))

    smtpSvr = smtplib.SMTP('express-smtp.cites.uiuc.edu')
    smtpSvr.set_debuglevel(1)

    print 'sending...'
    smtpSvr.sendmail(msg['From'], msg['To'], msg.as_string())
    smtpSvr.quit()
    print 'done.'


if __name__ == '__main__':
    main()
    pass

