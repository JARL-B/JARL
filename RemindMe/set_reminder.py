import discord
import time
import asyncio

from RemindMe.validate_event import count_reminders
from RemindMe.format_time import format_time
from RemindMe.globalvars import calendar

from get_patrons import get_patrons

async def set_reminder(message, client):
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
    await client.send_message(message.channel, embed=discord.Embed(description='Make sure the time you have provided is in the format of [num][s/m/h/d][num][s/m/h/d] etc. with no spaces, eg. 10s for 10 seconds or 10s12m15h1d for 10 seconds, 12 minutes, 15 hours and 1 day.'))
    return

  args.pop(0)

  msg_text = ' '.join(args)

  if count_reminders(scope) > 5 and message.author.id not in get_patrons('Donor'):
    await client.send_message(message.channel, embed=discord.Embed(description='Too many reminders in specified channel! Use `$del` to delete some of them, or use `$donate` to increase your maximum ($2 tier)'))
    return

  calendar.append([msg_time, scope, msg_text])

  await client.send_message(message.channel, embed=discord.Embed(description='New reminder registered for <{}> in {} seconds . You can\'t edit the reminder now, so you are free to delete the message.'.format(pref + scope, round(msg_time - time.time()))))
  print('Registered a new reminder for {}'.format(message.server.name))
