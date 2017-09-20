import discord
import asyncio
import sys
import os
import time

from globalvars import *

from get_help import get_help
from check_reminders import check_reminders
from change_prefix import change_prefix
from set_reminder import set_reminder
from set_event import set_event
from add_blacklist import add_blacklist
from get_time import get_time
from set_playing import set_playing
from create_issue import create_issue
from accept_invite import accept_invite
from transport import transport
from set_interval import set_interval
from del_reminders import del_reminders
from dev_tools import dev_tools
from donate import donate
from bind import bind
from update import update


async def blacklist_msg(message):
  msg = await client.send_message(message.channel, ':x: This text channel has been blacklisted :x:')
  await client.delete_message(message)
  await asyncio.sleep(2)
  await client.delete_message(msg)


command_map = {
  'help' : get_help,
  'remind' : set_reminder,
  'event' : set_event,
  'etime' : get_time,
  'playing' : set_playing,
  'blacklist' : add_blacklist,
  'suggestion' : create_issue,
  'issue' : create_issue,
  'invite' : accept_invite,
  'transport_me' : transport,
  'interval' : set_interval, ## patron only ##
  'del' : del_reminders,
  'dev' : dev_tools,
  'bind' : bind,
  'donate' : donate,
  'update' : update
}

@client.event ## print some stuff to console when the bot is activated
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    await client.change_presence(game=discord.Game(name='with ur calendar bb ;)'))


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
