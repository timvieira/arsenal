import sys, os, commands

def whatismyip2():
    """
    Alternative implementation of whatismyip based on different hacks.

    Implementation of this function borrowed from:
        woof -- an ad-hoc single file webserver
        Copyright (C) 2004-2009 Simon Budig  <simon@budig.de>
    """
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("gmail.com",80))
        ip = s.getsockname()[0]
    except: #socket.SocketError:
        return None
    finally:
        s.close()
    return ip

def whatismyip():
    """
    Utility function to guess the IP (as a string) where the server can be
    reached from the outside. Quite nasty problem actually. 

    Implementation of this function borrowed from:
        woof -- an ad-hoc single file webserver
        Copyright (C) 2004-2009 Simon Budig  <simon@budig.de>

    """
    if sys.platform == "cygwin":
        ipcfg = os.popen("ipconfig").readlines()
        for l in ipcfg:
          try:
             candidat = l.split(":")[1].strip()
             if candidat[0].isdigit():
                break
          except:
             pass
        return candidat
  
    os.environ["PATH"] = "/sbin:/usr/sbin:/usr/local/sbin:" + os.environ["PATH"]
    platform = os.uname()[0];
  
    if platform == "Linux":
        netstat = commands.getoutput("LC_MESSAGES=C netstat -rn")
        defiface = [i.split()[-1] for i in netstat.split('\n') if i.split()[0] == "0.0.0.0"]
    elif platform in ("Darwin", "FreeBSD", "NetBSD"):
        netstat = commands.getoutput("LC_MESSAGES=C netstat -rn")
        defiface = [i.split()[-1] for i in netstat.split('\n') if len(i) > 2 and i.split()[0] == "default"]
    elif platform == "SunOS":
        netstat = commands.getoutput("LC_MESSAGES=C netstat -arn")
        defiface = [i.split()[-1] for i in netstat.split('\n') if len(i) > 2 and i.split()[0] == "0.0.0.0"]
    else:
        print >>sys.stderr, "Unsupported platform; please add support for your platform in find_ip().";
        return None
 
    if not defiface:
        return None
 
    if platform == "Linux":
        ifcfg = commands.getoutput("LC_MESSAGES=C ifconfig " + defiface[0]).split("inet addr:")
    elif platform in ("Darwin", "FreeBSD", "SunOS", "NetBSD"):
        ifcfg = commands.getoutput("LC_MESSAGES=C ifconfig " + defiface[0]).split("inet ")
 
    if len(ifcfg) != 2:
        return None
    ip_addr = ifcfg[1].split()[0]
 
    # sanity check
    try:
        ints = [i for i in ip_addr.split(".") if 0 <= int(i) <= 255]
        if len(ints) != 4:
            return None
    except ValueError:
        return None
 
    return ip_addr
  

if __name__ == '__main__':
    print 'whatismyip: ', whatismyip()
    print 'whatismyip2:', whatismyip2()
