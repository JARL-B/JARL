import json
import queue
from RemindMe.Reminder import Reminder

print('Initializing RemindMe::globalvars.py')

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


calendar = [Reminder(dictv=r) for r in calendar]

print('Creating reminder queue')
reminders = queue.PriorityQueue()
[reminders.put(r) for r in calendar]
