import discord
import asyncio
import sys
import os
import time
import uuid
import re
import aiohttp

from globalvars import *

from Calc.pythagoras import pythagoras

from RemindMe.set_reminder import set_reminder
from RemindMe.set_event import set_event
from RemindMe.set_interval import set_interval
from RemindMe.del_reminders import del_reminders
from RemindMe.email_me import email_me
from RemindMe.todo import todo
from RemindMe.server_todo import server_todo

from TheManagement.autoclear import autoclear
from TheManagement.clear_channel import clear_channel
from TheManagement.spamfilter import spamfilter
from TheManagement.tagfilter import tagfilter
from TheManagement.profanityfilter import profanityfilter
from TheManagement.serverjoin import serverjoin
from TheManagement.serverleave import serverleave
from TheManagement.verification import verification
from TheManagement.vote import vote
from TheManagement.get_emails import get_emails

from Zalgo.zalgo import zalgo_call

from check_reminders import check_reminders
from change_prefix import change_prefix
from dev_tools import dev_tools
from add_blacklist import add_blacklist
from donate import donate
from update import update
from get_help import get_help
from register_email import register_email
from ping import ping


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
  'update' : update,
  #'clear' : clear_channel,
  'autoclear' : autoclear,
  'spam' : spamfilter,
  'tags' : tagfilter,
  'profanity' : profanityfilter,
  'joinmsg' : serverjoin,
  'leavemsg' : serverleave,
  'verif' : verification,
  'emails' : get_emails,
  'vote' : vote,
  'notify' : email_me,
  'todo' : todo,
  'todos' : server_todo,
  'zalgo' : zalgo_call,
  'pythagoras' : pythagoras,
  'ping' : ping
}

async def validate_cmd(message): ## method for doing the commands
  if message.server != None and message.server.id in prefix.keys():
    pref = prefix[message.server.id]
  else:
    pref = '$'

  if message.content[0] != pref: ## These functions call if the prefix isnt present
    if message.content.startswith('mbprefix'):

      if message.channel.id in channel_blacklist:
        await blacklist_msg(message)
        return

      await change_prefix(message)

    return

  cmd = message.content.split(' ')[0][1:] # extract the keyword
  if cmd in command_map.keys():

    if message.channel.id in channel_blacklist and cmd not in ['help', 'blacklist']:
      await blacklist_msg(message)

      return

    else:
      await command_map[cmd](message,client)

      return

async def watch_tags(message):
  if not (message.author.server_permissions.administrator or discord.utils.get(message.server.roles, name='Manager:Allow @here') in message.author.roles):
    if message.content.count('@everyone') + message.content.count('@here') > 1:
      await client.send_message(message.channel, 'Do not use `@everyone` or `@here`!')

      await client.ban(message.author)
      tag_warnings[message.author.id] = 2

      with open('DATA/tag_warnings.json','w') as f:
        json.dump(tag_warnings,f)

    elif '@everyone' in message.content or '@here' in message.content:
      await client.delete_message(message)

      if message.author.id not in tag_warnings.keys():
        tag_warnings[message.author.id] = 0

      tag_warnings[message.author.id] += 1
      await client.send_message(message.channel, 'Do not use `@everyone` or `@here`! ({}/4)'.format(tag_warnings[message.author.id]))

      if tag_warnings[message.author.id] > 3:
        await client.ban(message.author)
        tag_warnings[message.author.id] = 0

      with open('DATA/tag_warnings.json','w') as f:
        json.dump(tag_warnings,f)


async def watch_spam(message):
  if message.author.id in users.keys(): ## all the stuff to do with smap filtering
    if time.time() - users[message.author.id] < 2:

      if message.author.id in warnings.keys():

        warnings[message.author.id] += 1
        if warnings[message.author.id] == 4:
          await client.send_message(message.channel, 'Please slow down {}'.format(message.author.mention))

        elif warnings[message.author.id] == 6:

          overwrite = discord.PermissionOverwrite()
          overwrite.send_messages = False
          await client.edit_channel_permissions(message.channel, message.author, overwrite)
          await client.send_message(message.channel, '{}, you\'ve been muted for spam. Please contact an admin to review your status.'.format(message.author.mention))

      else:
        print('user added to warning list')
        warnings[message.author.id] = 1

      users[message.author.id] = time.time()

    else:
      users[message.author.id] = time.time()
      warnings[message.author.id] = 0

  else:
    print('registered user for auto-muting')
    users[message.author.id] = time.time()

async def watch_profanity(message):
  compressed = message.content.replace(' ','').replace('-','').replace('_','').replace('^','').replace('\'','').replace('\"','').replace('=','').replace('*','')
  uid = uuid.uuid4()
  with open('profanity.exp','r') as f:
    for reg in f:
      reg = reg.strip()
      exp = re.search(reg,compressed)
      if exp: ## perform a regex search for illicit terms
        with open('DATA/profanity_issues','a') as f2:
          f2.write('{} term detected at {} (UUID {})\n'.format(exp.group(),message.author.name,uid))
        print('{} term detected at {} (UUID {})'.format(exp.group(),message.author.name,uid))
        await client.send_message(message.channel, 'Illicit term detected in input {}. If you believe this warning has been administered wrongly, please send the code `{}` to the support channel in the Discord group'.format(message.author.mention,uid))
        await client.delete_message(message)
        return

async def send():
  session = aiohttp.ClientSession()
  dump = json.dumps({
    'server_count': len(client.servers)
  })

  head = {
    'authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjM0OTkyMDA1OTU0OTk0MTc2MSIsImJvdCI6dHJ1ZSwiaWF0IjoxNTA4NzU1OTA1fQ.p59GEanXurNBXskgoH-TivkPlU3n-soNeeC2VrPX6zU',
    'content-type' : 'application/json'
  }

  url = 'https://discordbots.org/api/bots/stats'
  async with session.post(url, data=dump, headers=head) as resp:
    print('returned {0.status} for {1}'.format(resp, dump))

  session.close()

@client.event ## print some stuff to console when the bot is activated
async def on_ready():
  print('Logged in as')
  print(client.user.name)
  print(client.user.id)
  print('------')

  #await send()

  await client.change_presence(game=discord.Game(name='$help ¬ mbprefix <p>'))

@client.event
async def on_server_join(server):
    await send()

@client.event
async def on_server_remove(server):
    await send()

@client.event
async def on_message(message): ## when a message arrives at the bot ##
  if message.author.id == client.user.id: ## if the message has been sent by the bot ##
    return

  if message.content in ['', None]: ## if the message is a file ##
    return

  try:
    await validate_cmd(message)

    ## run stuff here if there is no command ##
    if message.channel.id in autoclears.keys(): ## autoclearing
      await asyncio.sleep(autoclears[message.channel.id])
      await client.delete_message(message)

    if message.channel.id in spam_filter:
      await watch_spam(message)

    if message.channel.id in profanity_filter:
      await watch_profanity(message)

    if message.channel.id in tag_filter:
      await watch_tags(message)
  except discord.errors.Forbidden:
    try:
      await client.send_message(message.channel, 'Failed to perform an action: Not enough permissions (403)')
    except discord.errors.Forbidden:
      try:
        await client.send_message(message.author, 'Failed to perform actions on {}: Not enough permissions (403)'.format(message.server.name))
      except discord.errors.Forbidden:
        pass

@client.event
async def on_member_join(member):
  if member.server.id in join_messages.keys():
    try:
      await client.send_message(client.get_channel(join_messages[member.server.id][1]),join_messages[member.server.id][0].format(member.name))
    except:
      print('Issue encountered administering member join message.')

  if member.server.id in verif_servers:
    await register_email(member)

@client.event
async def on_member_remove(member):
  if member.server.id in leave_messages.keys():
    try:
      await client.send_message(client.get_channel(leave_messages[member.server.id][1]),leave_messages[member.server.id][0].format(member.name))
    except:
      print('Issue encountered administering member leave message.')

@client.event
async def on_reaction_add(reaction, user):
  for v in votes:
    if reaction.message.id == v.message.id:
      if reaction.emoji == '❎':
        v.neg_v += 1
      elif reaction.emoji == '✅':
        v.pos_v += 1
      return

try: ## token grabbing code
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
