import discord
import json

autoclears = {}
users = {}
warnings = {}

spam_filter = []
profanity_filter = []

try:
  with open('DATA/autoclears.json','r') as f:
    autoclears = json.load(f)

except FileNotFoundError:
  print('no autoclear file found')

try:
  with open('DATA/spamfilter','r') as f:
    spam = f.read().strip('\n')
    spam = ''.join(spam)
    spam_filter = spam.split(',')

except FileNotFoundError:
  print('no spam filter file found')

try:
  with open('DATA/profanityfilter','r') as f:
    prof = f.read().strip('\n')
    prof = ''.join(prof)
    profanity_filter = prof.split(',')

except FileNotFoundError:
  print('no profanity filter file found')
