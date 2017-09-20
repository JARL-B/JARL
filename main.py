import discord
import asyncio
import sys
import os
import time

from globalvars import *

from RemindMe.check_reminders import check_reminders
from RemindMe.set_reminder import set_reminder
from RemindMe.set_event import set_event
from RemindMe.set_interval import set_interval
from RemindMe.del_reminders import del_reminders

from change_prefix import change_prefix
from dev_tools import dev_tools
from add_blacklist import add_blacklist
from donate import donate
from update import update
from get_help import get_help


async def blacklist_msg(message):
  msg = await client.send_message(message.channel, ':x: This text channel has been blacklisted :x:')
  await client.delete_message(message)
  await asyncio.sleep(2)
  await client.delete_message(msg)


command_map = {
  'help' : get_help,
  'remind' : set_reminder,
  'event' : set_event,
  'blacklist' : add_blacklist,
  'interval' : set_interval, ## patron only ##
  'del' : del_reminders,
  'dev' : dev_tools,
  'donate' : donate,
  'update' : update
}

@client.event ## print some stuff to console when the bot is activated
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message): ## when a message arrives at the bot ##
  if message.author.id == client.user.id:
    return

  if message.content in ['', None]:
    return

  cmd_content = message.content.lower()

  if message.server != None and message.server.id in prefix.keys():
    pref = prefix[message.server.id]
  else:
    pref = '$'

  if message.content[0] != pref: ## These functions call if the prefix isnt present
    if message.content.startswith('rbprefix'):

      if message.channel.id in channel_blacklist:
        await blacklist_msg(message)
        return

      await change_prefix(message)

    return

  cmd = cmd_content.split(' ')[0][1:] # extract the keyword
  if cmd in command_map.keys():

    if message.channel.id in channel_blacklist and cmd != 'help':
      await blacklist_msg(message)

      return

    else:
      await command_map[cmd](message)

      return

try:
  with open('token','r') as token_f:
    token = token_f.read().strip('\n')

except FileNotFoundError:
  if len(sys.argv) < 2:
    print('Please remember you need to enter a token for the bot as an argument, or create a file called \'token\' and enter your token into it.')
  else:
    token = sys.argv[1]

else:
  try:
    client.loop.create_task(check_reminders())
    client.run(token)
  except:
    print('Error detected. Restarting in 15 seconds.')
    time.sleep(15)

    os.execl(sys.executable, sys.executable, *sys.argv)
