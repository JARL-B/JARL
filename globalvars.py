from RemindMe.globalvars import *

client = discord.Client() ## defined the client

try:
  with open('prefix','r') as f:
    pref = f.read().strip()
    pref = ''.join(pref)
    pref = pref.split(';')

    for item in pref:
      if len(item) < 2:
        pref.remove(item)

    for item in pref:
      item = item.split(',')
      if item[1] == '$':
        continue
      prefix[item[0]] = item[1]

except FileNotFoundError:
  print('no prefix file found')

try:
  with open('blacklist','r') as f:
    bl = f.read().strip('\n')
    bl = ''.join(bl)
    channel_blacklist = bl.split(',')

except FileNotFoundError:
  print('no blacklist file found')
