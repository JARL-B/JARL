import json
from RemindMe.Reminder import Reminder

mail_list = {}
calendar = []
intervals = []
todos = {}
timezones = {}

try:
  with open('DATA/calendar.json', 'r') as f:
    calendar = json.load(f)

except FileNotFoundError:
  print('no calendar file found. not loading any reminders')
  with open('DATA/calendar.json', 'w') as f:
    f.write("[]")
  print('created calendar file')

try:
  with open('DATA/intervals.json', 'r') as f:
    intervals = json.load(f)

except FileNotFoundError:
  print('no interval file found. not loading any intervals')
  with open('DATA/intervals.json', 'w') as f:
    f.write("[]")
  print('created intervals file')

try:
  with open('DATA/todos.json','r') as f:
    todos = json.load(f)

  todos = {int(x) : y for x, y in todos.items()}

except FileNotFoundError:
  print('no todos file found.')
  with open('DATA/todos.json', 'w') as f:
    f.write("{}")
  print('created todos file')

try:
  with open('DATA/timezones.json','r') as f:
    timezones = json.load(f)

except FileNotFoundError:
  print('no timezones file found.')
  with open('DATA/timezones.json', 'w') as f:
    f.write("{}")
  print('created timezones file')

if len(calendar) > 0 and isinstance(calendar[0], list):
  calendar = [Reminder(dictv={'time' : x, 'channel' : int(y), 'message' : z, 'interval' : None}) for x, y, z in calendar] # NOT NECESSARY PAST FIRST RELAUNCH: convert list of lists to dictionary
  intervals = [Reminder(dictv={'time' : x, 'interval' : y, 'channel' : int(z), 'message' : a}) for x, y, z, a in intervals]

else:
  calendar = [Reminder(dictv=r) for r in calendar]
  intervals = [Reminder(dictv=r) for r in intervals]
