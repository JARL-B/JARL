import json

from RemindMe.globalvars import *

client = discord.Client() ## defined the client

prefix = {}
blacklist = []

try:
  with open('prefix.json','r') as f: ## TODO change to JSON file
    prefix = json.load(f)

except:
  print('no prefix file found')

try:
  with open('blacklist','r') as f:
    bl = f.read().strip('\n')
    bl = ''.join(bl)
    channel_blacklist = bl.split(',')

except FileNotFoundError:
  print('no blacklist file found')
