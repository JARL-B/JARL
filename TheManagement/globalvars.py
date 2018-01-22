import discord
import json

autoclears = {}
users = {}
warnings = {}
join_messages = {}
leave_messages = {}
terms = {}

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
  with open('DATA/spamfilter.json', 'r') as f:
    spam_filter = json.load(f)

  spam_filter = list(map(int, spam_filter))

except FileNotFoundError:
  print('no spam filter file found')
  with open('DATA/spamfilter.json', 'w') as f:
    f.write("[]")
  print('created spamfilter file')

try:
  with open('DATA/join_messages.json', 'r') as f:
    join_messages = json.load(f)

  join_messages = {int(x) : [y[0], int(y[1])] for x, y in join_messages.items()}

except FileNotFoundError:
  print('no join messages file found')
  with open('DATA/join_messages.json', 'w') as f:
    f.write("{}")
  print('created join messages file')

try:
  with open('DATA/leave_messages.json', 'r') as f:
    leave_messages = json.load(f)

  leave_messages = {int(x) : [y[0], int(y[1])] for x, y in leave_messages.items()}

except FileNotFoundError:
  print('no leave messages file found')
  with open('DATA/leave_messages.json', 'w') as f:
    f.write("{}")
  print('created leave messages file')
