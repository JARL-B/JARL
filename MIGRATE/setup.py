import os
import sqlite3
import configparser

try:
    os.mkdir('../DATA')
except FileExistsError:
    pass

files = ['autoclears', 'blacklist', 'join_messages', 'leave_messages', 'prefix', 'restrictions', 'spamfilter', 'tags', 'timezones', 'todos']
contents = ['{}', '[]', '{}', '{}', '{}', '{}', '[]', '{}', '{}', '{}']

for fn, content in zip(files, contents):
    if fn + '.json' in os.listdir('../DATA/'):
        continue

    f = open('../DATA/' + fn + '.json', 'w')
    f.write(content)
    f.close()

try:
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
except sqlite3.OperationalError:
    print('Skipping table generation')

try:
    connection = sqlite3.connect('../DATA/calendar.db')
    cursor = connection.cursor()

    command = '''CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    token VARCHAR(32)
    );'''

    cursor.execute(command)
    connection.commit()
    connection.close()
except sqlite3.OperationalError:
    print('Skipping user table generation')

if 'config.ini' not in os.listdir('..'):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {
        'token' : 'token',
        'dbl_token' : 'discordbotslist token',
        'patreon_server' : 'serverid',
        'patreon_enabled' : 'yes'
    }

    with open('../config.ini', 'w') as f:
        config.write(f)
