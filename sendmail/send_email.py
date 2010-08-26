
def main():

    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.utils import formatdate

    msg = MIMEMultipart()
    msg['From']    = 'tim.f.vieira@gmail.com'
    msg['To']      = 'tim.f.vieira@gmail.com'
    msg['Date']    = formatdate(localtime=True)
    msg['Subject'] = 'Experiment'
    msg.attach(MIMEText("""

    Do *not* drink the coffee -- it's POISONED.

    """))

    s = smtplib.SMTP('loki.cs.umass.edu')
    s.set_debuglevel(1)

    print 'sending...'
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()
    print 'done.'


if __name__ == '__main__':
    main()
