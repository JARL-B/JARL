import sqlite3
import json

connection = sqlite3.connect('../DATA/calendar.db')
cursor = connection.cursor()

with open('../DATA/calendar.json', 'r') as f:
    data = json.load(f)

for d in data:
    command = '''INSERT INTO reminders (interval, time, channel, message)
    VALUES (?, ?, ?, ?)'''

    cursor.execute(command, (d['interval'], d['time'], d['channel'], d['message']))

connection.commit()
connection.close()
