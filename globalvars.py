import json
import smtplib

from RemindMe.globalvars import *
from TheManagement.globalvars import *

from gmail import gmail

client = discord.Client() ## defined the client

prefix = {}
wiki_cache = {}
channel_blacklist = []

try:
  with open('DATA/prefix.json','r') as f:
    prefix = json.load(f)

except:
  print('no prefix file found')

try:
  with open('DATA/blacklist.json','r') as f:
    channel_blacklist = json.load(f)

except FileNotFoundError:
  print('no blacklist file found')

mailserver = gmail()
