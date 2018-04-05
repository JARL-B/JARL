import discord
import json

print('Initializing TheManagement::globalvars.py')

autoclears = {}
users = {}
warnings = {}
join_messages = {}
leave_messages = {}
terms = {}
tags = {}

spam_filter = []

try:
    with open('DATA/autoclears.json', 'r') as f:
        autoclears = json.load(f)

    autoclears = {int(x) : y for x, y in autoclears.items()}

except FileNotFoundError:
    print('no autoclear file found')
    with open('DATA/autoclears.json', 'w') as f:
        f.write("{}")
    print('created autoclear file')


try:
    with open('DATA/tags.json', 'r') as f:
        tags = json.load(f)

    tags = {int(x) : y for x, y in tags.items()}

except FileNotFoundError:
    print('no tags file found')
    with open('DATA/tags.json', 'w') as f:
        f.write('{}')
    print('created tags file')
