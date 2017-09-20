import discord
import json

autoclears = {}
users = {}
warnings = {}

try:
  with open('autoclears.json','r') as f:
    autoclears = json.load(f)

except FileNotFoundError:
  print('no autoclear file found')
