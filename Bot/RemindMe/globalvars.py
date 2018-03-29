import json
import sqlite3
from RemindMe.Reminder import Reminder

print('Initializing RemindMe::globalvars.py')

todos = {}
timezones = {}

variables = [
    'todos',
    'timezones'
]

for variable in variables:
    try:
        with open('DATA/{}.json'.format(variable), 'r') as f:
            exec('{} = json.load(f)'.format(variable))

    except FileNotFoundError:
        with open('DATA/{}.json'.format(variable), 'w') as f:
            exec('json.dump({}, f)'.format(variable))
        print('created {} file'.format(variable))

todos = {int(x) : y for x, y in todos.items()}

reminders = []

connection = sqlite3.connect('DATA/calendar.db') #open SQL db
cursor = connection.cursor() #place cursor
cursor.row_factory = sqlite3.Row #set row to read as SQLite Rows

cursor.execute('SELECT * FROM reminders') #select all rows
for reminder in cursor.fetchall(): #for all rows...
    reminders.append(Reminder(dictv=dict(reminder))) #place each in the list

reminders.sort(key=lambda x: x.time)
