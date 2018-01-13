import discord
import json

autoclears = {}
users = {}
warnings = {}
tag_warnings = {}
join_messages = {}
leave_messages = {}
terms = {}

spam_filter = []
profanity_filter = []
tag_filter = []

emails = {}
verif_servers = []

votes = []

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
  with open('DATA/profanityfilter.json','r') as f:
    profanity_filter = json.load(f)

except FileNotFoundError:
  print('no profanity filter file found')

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
  with open('DATA/verif_servers.json','r') as f:
    verif_servers = json.load(f)

except FileNotFoundError:
  print('no verif servers file found')

try:
  with open('DATA/emails.json','r') as f:
    emails = json.load(f)

except FileNotFoundError:
  print('no emails file found')

try:
  with open('DATA/tag_warnings.json','r') as f:
    tag_warnings = json.load(f)

except FileNotFoundError:
  print('no tag warnings file found')

try:
  with open('DATA/tag_filter.json','r') as f:
    tag_filter = json.load(f)

except FileNotFoundError:
  print('no tag filter file found')

try:
  with open('DATA/terms.json','r') as f:
    terms = json.load(f)

except FileNotFoundError:
  print('no terms filter file found')
