import json

mail_list = {}
calendar = []
intervals = []
todos = {}

try:
  with open('DATA/calendar.json', 'r') as f:
    calendar = json.load(f)

  calendar = [[x, int(y), z] for x, y, z in calendar]

except FileNotFoundError:
  try:
    with open('DATA/calendar.csv', 'r') as f:
      cal = f.read()
      cal = cal.strip()
      cal = ''.join(cal)
      cal = cal.split(';')

      for item in cal:
        item = item.split(',')
        calendar.append(item)

    calendar = [[x, int(y), z] for x, y, z in calendar]

  except FileNotFoundError:
    print('no calendar file found. not loading any reminders')

try:
  with open('DATA/intervals.json', 'r') as f:
    intervals = json.load(f)

  intervals = [[x, y, int(z), a] for x, y, z, a in intervals]

except FileNotFoundError:
  try:
    with open('DATA/intervals.csv','r') as f:
      inv = f.read()
      inv = inv.strip()
      inv = ''.join(inv)
      inv = inv.split(';')

      for item in inv:
        item = item.split(',')
        intervals.append(item)

    intervals = [[x, y, int(z), a] for x, y, z, a in intervals]

  except FileNotFoundError:
    print('no interval file found. not loading any intervals')

try:
  with open('DATA/todos.json','r') as f:
    todos = json.load(f)

  todos = {int(x) : y for x, y in todos.items()}

except FileNotFoundError:
  print('no todos file found.')

for reminder in calendar:
  if len(reminder) != 3:
    calendar.remove(reminder)

for inv in intervals:
  if len(inv) != 4:
    intervals.remove(inv)
