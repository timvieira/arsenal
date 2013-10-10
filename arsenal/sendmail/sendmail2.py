import subprocess
import email.Utils

def safestr(obj, encoding='utf-8'):
    r"""
    Converts any given object to utf-8 encoded string. 
    
        >>> safestr('hello')
        'hello'
        >>> safestr(u'\u1234')
        '\xe1\x88\xb4'
        >>> safestr(2)
        '2'
    """
    if isinstance(obj, unicode):
        return obj.encode('utf-8')
    elif isinstance(obj, str):
        return obj
    elif hasattr(obj, 'next') and hasattr(obj, '__iter__'): # iterator
        return itertools.imap(safestr, obj)
    else:
        return str(obj)


def sendmail(from_address, to_address, subject, message, **kw):
    """
    Sends the email message `message` with mail and envelope headers for from 
    `from_address_` to `to_address` with `subject`. Additional email headers
    can be specified with the dictionary  `headers.

    Uses `/usr/sbin/sendmail`, (the typical location for the sendmail binary).
    """
        
    cc = kw.get('cc', [])
    bcc = kw.get('bcc', [])
    
    def listify(x):
        if not isinstance(x, list):
            return [safestr(x)]
        else:
            return [safestr(a) for a in x]

    from_address = safestr(from_address)

    to_address = listify(to_address)
    cc = listify(cc)
    bcc = listify(bcc)

    recipients = to_address + cc + bcc
    
    headers = {
      'MIME-Version': '1.0',
      'Content-Type': 'text/plain; charset=UTF-8',
      'Content-Disposition': 'inline',
      'From': from_address,
      'To': ", ".join(to_address),
      'Subject': subject
    }

    if cc:
        headers['Cc'] = ", ".join(cc)    

    from_address = email.Utils.parseaddr(from_address)[1]
    recipients = [email.Utils.parseaddr(r)[1] for r in recipients]
    message = ('\n'.join([safestr('%s: %s' % x) for x in headers.iteritems()])
               + "\n\n" +  safestr(message))

    sendmail = '/usr/sbin/sendmail'
    
    assert not from_address.startswith('-'), 'security'
    for r in recipients:
        assert not r.startswith('-'), 'security'

    p = subprocess.Popen(['/usr/sbin/sendmail', '-f', from_address] + recipients, stdin=subprocess.PIPE)
    p.stdin.write(message)
    p.stdin.close()
    p.wait()


if __name__ == '__main__':
    sendmail('test@herman.local', 'tim.f.vieira@gmail.com', 'this is a test', 'See subject.')
