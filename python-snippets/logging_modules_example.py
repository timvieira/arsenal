
import logging
import logging.handlers

LOG_FILENAME = 'my-log-file'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

logging.debug('This message should go to the log file')


logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical error message')


print '***********************************************'
print '** log file contents:'
with file(LOG_FILENAME,'rb') as f:
    print f.read()
print '***********************************************'


my_logger = logging.getLogger('my-logger')

#smtp = 'smtp.gmail.com'
#smtp = 'mail-auth.oit.umass.edu'
#smtp = 'express-smtp.cites.uiuc.edu'
#email_handler = logging.handlers.SMTPHandler(smtp, 'tim.f.vieira@gmail.com', 'tim.f.vieira@gmail.com', 'Critical message from system.')
#my_logger.addHandler(email_handler)
#my_logger.critical('critical message from your script.')



