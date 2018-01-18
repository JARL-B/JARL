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
  with open('DATA/autoclears.json','r') as f:
    autoclears = json.load(f)

except FileNotFoundError:
  print('no autoclear file found')

try:
  with open('DATA/spamfilter.json','r') as f:
    spam_filter = json.load(f)

except FileNotFoundError:
  print('no spam filter file found')

try:
  with open('DATA/join_messages.json','r') as f:
    join_messages = json.load(f)

except FileNotFoundError:
  print('no join messages file found')

try:
  with open('DATA/leave_messages.json','r') as f:
    leave_messages = json.load(f)

except FileNotFoundError:
  print('no leave messages file found')

try:
  with open('DATA/terms.json','r') as f:
    terms = json.load(f)

except FileNotFoundError:
  print('no terms filter file found')
