import json

from RemindMe.globalvars import *
from TheManagement.globalvars import *

client = discord.Client() ## defined the client

prefix = {}
channel_blacklist = []

try:
  with open('DATA/prefix.json','r') as f:
    prefix = json.load(f)

except:
  print('no prefix file found')

try:
  with open('DATA/blacklist','r') as f:
    bl = f.read().strip('\n')
    bl = ''.join(bl)
    channel_blacklist = bl.split(',')

except FileNotFoundError:
  print('no blacklist file found')
