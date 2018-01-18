import json

mail_list = {}
calendar = []
intervals = []
todos = {}

try:
  with open('DATA/calendar.csv','r') as f:
    cal = f.read()
    cal = cal.strip()
    cal = ''.join(cal)
    cal = cal.split(';')

    for item in cal:
      item = item.split(',')
      calendar.append(item)

except FileNotFoundError:
  print('no calendar file found. not loading any reminders')

try:
  with open('DATA/intervals.csv','r') as f:
    inv = f.read()
    inv = inv.strip()
    inv = ''.join(inv)
    inv = inv.split(';')

    for item in inv:
      item = item.split(',')
      intervals.append(item)

except FileNotFoundError:
  print('no interval file found. not loading any intervals')

try:
  with open('DATA/todos.json','r') as f:
    todos = json.load(f)

except FileNotFoundError:
  print('no todos file found.')

for reminder in calendar:
  if len(reminder) != 3:
    calendar.remove(reminder)

for inv in intervals:
  if len(inv) != 4:
    intervals.remove(inv)
