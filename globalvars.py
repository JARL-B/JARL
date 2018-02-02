import json

from RemindMe.globalvars import *
from TheManagement.globalvars import *

client = discord.Client() ## defined the client

prefix = {}
restrictions = {}
channel_blacklist = []

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