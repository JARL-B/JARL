import os
import sqlite3

try:
    os.mkdir('../DATA')
except FileExistsError:
    pass

files = ['autoclears', 'blacklist', 'join_messages', 'leave_messages', 'log', 'prefix', 'restrictions', 'spamfilter', 'tags', 'timezones', 'todos']
contents = ['{}', '[]', '{}', '{}', '{}', '{}', '{}', '[]', '{}', '{}', '{}']

for fn, content in zip(files, contents):
    if fn + '.json' in os.listdir('../DATA/'):
        continue

    f = open('../DATA/' + fn + '.json', 'w')
    f.write(content)
    f.close()

connection = sqlite3.connect('../DATA/calendar.db')
cursor = connection.cursor()

command = '''CREATE TABLE reminders (
interval INTEGER,
time INTEGER,
message VARCHAR(400),
channel INTEGER
);'''

cursor.execute(command)
connection.commit()
connection.close()
