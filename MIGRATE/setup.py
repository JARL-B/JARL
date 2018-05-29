import os
import sqlite3
import configparser

try:
    os.mkdir('../DATA')
except FileExistsError:
    pass

files = ['todos']
contents = ['{}']

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
    message VARCHAR(1900),
    channel INTEGER
    );'''

    cursor.execute(command)
    connection.commit()
    connection.close()
except sqlite3.OperationalError:
    print('Skipping table generation')

try:
    with sqlite3.connect('../DATA/calendar.db') as connection:
        cursor = connection.cursor()

        command = '''CREATE TABLE servers (
        id INTEGER,
        prefix VARCHAR,
        timezone VARCHAR,
        language VARCHAR,
        blacklist VARCHAR,
        restrictions VARCHAR,
        tags VARCHAR,
        autoclears VARCHAR
        )'''

        cursor.execute(command)
        connection.commit()

except sqlite3.OperationalError:
    print('Skipping server table gen')

try:
    with sqlite3.connect('../DATA/calendar.db') as connection:
        cursor = connection.cursor()

        command = '''CREATE TABLE connections (
        id INTEGER,
        users VARCHAR
        )'''

        cursor.execute(command)
        connection.commit()

except sqlite3.OperationalError:
    print('Skipping connection table gen')


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
