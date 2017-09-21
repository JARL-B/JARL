import discord
import json

autoclears = {}
users = {}
warnings = {}

spam_filter = []
profanity_filter = []

try:
  with open('autoclears.json','r') as f:
    autoclears = json.load(f)

except FileNotFoundError:
  print('no autoclear file found')
