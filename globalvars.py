import time
import json
import configparser

from RemindMe.globalvars import *
from TheManagement.globalvars import *

print('Initializing main::globalvars.py')

client = discord.Client() ## defined the client

prefix = {}
restrictions = {}
channel_blacklist = []

times = {
    'last_loop' : time.time(),
    'start' : 0,
    'loops' : 0
}

try:
    with open('DATA/prefix.json','r') as f:
        prefix = json.load(f)

    prefix = {int(x) : y for x, y in prefix.items()}

except:
    print('no prefix file found')
    with open('DATA/prefix.json', 'w') as f:
        f.write("{}")
    print('prefix file created')

try:
    with open('DATA/blacklist.json','r') as f:
        channel_blacklist = json.load(f)

    channel_blacklist = list(map(int, channel_blacklist))

except FileNotFoundError:
    print('no blacklist file found')
    with open('DATA/blacklist.json', 'w') as f:
        f.write("[]")
    print('created blacklist file')

try:
    with open('DATA/restrictions.json','r') as f:
        restrictions = json.load(f)

    restrictions = {int(x) : list(map(int, y)) for x, y in restrictions.items()}

except FileNotFoundError:
    print('no restrictions file found')
    with open('DATA/restrictions.json', 'w') as f:
        f.write("{}")
    print('created restrictions file')

config = configparser.SafeConfigParser()
config.read('config.ini')
dbl_token = config.get('DEFAULT', 'dbl_token')
patreon = config.get('DEFAULT', 'patreon_enabled') == 'yes'
patreonserver = int(config.get('DEFAULT', 'patreon_server'))

if patreon:
    print('Patreon is enabled. Will look for server {}'.format(patreonserver))
