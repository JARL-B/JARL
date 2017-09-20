import discord
import asyncio

client = discord.Client() ## defined the client

prefix = {}
channel_blacklist = []
calendar = []
intervals = []
binds = {}

try:
  with open('calendar','r') as f:
    cal = f.read()
    cal = cal.strip()
    cal = ''.join(cal)
    cal = cal.split(';')

    for item in cal:
      item = item.split(',')
      calendar.append(item)

except FileNotFoundError:
  print('no calendar file found. not loading any reminders')

try:
  with open('intervals','r') as f:
    inv = f.read()
    inv = inv.strip()
    inv = ''.join(inv)
    inv = inv.split(';')

    for item in inv:
      item = item.split(',')
      intervals.append(item)

except FileNotFoundError:
  print('no interval file found. not loading any intervals')

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


for reminder in calendar:
  if len(reminder) != 3:
    calendar.remove(reminder)

for inv in intervals:
  if len(inv) != 4:
    intervals.remove(inv)

for item in channel_blacklist:
  if len(item) < 3:
    channel_blacklist.remove(item)

print(calendar)
print(intervals)
print(channel_blacklist)
print(prefix)
