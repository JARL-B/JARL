import discord
import asyncio
import time

from RemindMe.format_time import format_time
from RemindMe.globalvars import intervals

from get_patrons import get_patrons

async def set_interval(message, client):

  if message.author not in get_patrons('Donor'):
    await client.send_message(message.channel, embed=discord.Embed(description='You need to be a Patron (donating 2$ or more) to access this command! Type `$donate` to find out more.'))
    return

  args = message.content.split(' ')
  args.pop(0) # remove the command item

  scope = message.channel.id
  pref = '#'

  if args[0].startswith('<'): # if a scope is provided
    tag = args[0][2:-1]

    if args[0][1] == '@': # if the scope is a user
      pref = '@'
      scope = message.server.get_member(tag)

    else:
      pref = '#'
      scope = message.server.get_channel(tag)

    if scope == None:
      await client.send_message(message.channel, embed=discord.Embed(description='Couldn\'t find a person by your tag present.'))
      return

    else:
      scope = scope.id

    args.pop(0)

  msg_time = format_time(args[0])

  if msg_time == None:
    await client.send_message(message.channel, embed=discord.Embed(description='Make sure the time you have provided is in the format of [num][s/m/h/d][num][s/m/h/d] etc. or `day`/`month`/`year`-`hour`:`minute`:`second`.'))
    return

  args.pop(0)

  msg_interval = round(format_time(args[0]) - time.time())

  if msg_interval == None:
    await client.send_message(message.channel, embed=discord.Embed(description='Make sure the interval you have provided is in the format of [num][s/m/h/d][num][s/m/h/d] etc. with no spaces, eg. 10s for 10 seconds or 10s12m15h1d for 10 seconds, 12 minutes, 15 hours and 1 day.'))
    return
  elif msg_interval < 8:
    await client.send_message(message.channel, embed=discord.Embed(description='Please make sure your interval timer is longer than 8 seconds.'))
    return

  args.pop(0)

  msg_text = ' '.join(args)

  if pref == '#':
    if not message.author.server_permissions.administrator:
      if scope not in restrictions.keys():
        restrictions[scope] = []
      for role in message.author.roles:
        if role.id in restrictions[scope]:
          break
      else:
        await client.send_message(message.channel, embed=discord.Embed(description='You must be either admin or have a role capable of sending reminders to that channel. Please talk to your server admin, and tell her/him to use the `$restrict` command to specify allowed roles.'))
        return

  intervals.append([msg_time, msg_interval, scope, msg_text])

  await client.send_message(message.channel, embed=discord.Embed(description='New interval registered for <{}> in {} seconds . You can\'t edit the reminder now, so you are free to delete the message.'.format(pref + scope, round(msg_time - time.time()))))
  print('Registered a new interval for {}'.format(message.server.name))
