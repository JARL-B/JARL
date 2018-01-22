import json

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

for reminder in calendar:
  if len(reminder) != 3:
    calendar.remove(reminder)

for inv in intervals:
  if len(inv) != 4:
    intervals.remove(inv)

calendar = [[x, int(y), z] for x, y, z in calendar]
intervals = [[x, y, int(z), a] for x, y, z, a in intervals]
