#!/usr/bin/env python

import os, sys, getpass

from gcal import atom, gdata
import gdata.calendar
import gdata.calendar.service

email = 'timsfanmail'
password = getpass.getpass()

cal_client = gdata.calendar.service.CalendarService(email, password, 'Google-Calendar_Python_Sample-1.0')
cal_client.ProgrammaticLogin()

def quickadd(content):
    event = gdata.calendar.CalendarEventEntry()
    event.content   = atom.Content(text=content)
    event.quick_add = gdata.calendar.QuickAdd(value='true')
    new_event = cal_client.InsertEvent(event, '/calendar/feeds/default/private/full')

quickadd(' '.join(sys.argv[1:]))
os.system('firefox http://google.com/calendar 2>/dev/null &')
