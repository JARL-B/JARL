import time
from datetime import datetime

from RemindMe.globalvars import timezones

def format_time(text, guildid):
  if '/' in text or ':' in text:
    date = datetime.now()

    year = date.year
    month = date.month
    day = date.day
    hour = date.hour
    minute = date.minute
    second = date.second

    for clump in text.split('-'):
      if '/' in clump:
        a = clump.split('/')
        if len(a) == 2:
          month = a[1]
          day = a[0]
        elif len(a) == 3:
          year = a[2]
          month = a[1]
          day = a[0]

      elif ':' in clump:
        a = clump.split(':')
        if len(a) == 2:
          hour = a[0]
          minute = a[1]
        elif len(a) == 3:
          hour = a[0]
          minute = a[1]
          second = a[2]
        else:
          return None

      else:
        day = clump

    comp = '{}/{}/{}-{}:{}:{}'.format(day, month, year, hour, minute, second)
    try:
      t = datetime.strptime(comp, "%d/%m/%Y-%H:%M:%S").timestamp()
      if guildid in timezones.keys():
        t -= timezones[guildid]
    except Exception as e:
      t = None

    return t

  else:
    current_buffer = '0'
    seconds = 0
    minutes = 0
    hours = 0
    days = 0

    for char in text:

      if char == 's':
        seconds = int(current_buffer)
        current_buffer = '0'

      elif char == 'm':
        minutes = int(current_buffer)
        current_buffer = '0'

      elif char == 'h':
        hours = int(current_buffer)
        current_buffer = '0'

      elif char == 'd':
        days = int(current_buffer)
        current_buffer = '0'

      else:
        try:
          int(char)
          current_buffer += char
        except ValueError:
          return None

    time_sec = round(time.time() + seconds + (minutes * 60) + (hours * 3600) + (days * 86400) + int(current_buffer))
    return time_sec
