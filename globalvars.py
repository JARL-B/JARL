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

except:
  print('no prefix file found')

try:
  with open('DATA/blacklist.json','r') as f:
    channel_blacklist = json.load(f)

except FileNotFoundError:
  print('no blacklist file found')

try:
  with open('DATA/restrictions.json','r') as f:
    restrictions = json.load(f)

except FileNotFoundError:
  print('no restrictions file found')
