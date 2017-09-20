import discord
import asyncio
import time

from globalvars import *
from format_time import format_time
from get_patrons import get_patrons
from get_binds import get_binds

async def set_interval(message, client):
  if message.author in get_patrons(level='Donor') or message.server.id in get_binds():
    if ',' in message.content or ';' in message.content:
      await client.send_message(message.channel, 'Sorry, but you cannot place commas or semi-colons inside your reminders due to storage formats')
    else:
      text = message.content.split(' ')
      text.pop(0) ## remove the command item

      msg_time = text.pop(0) ## pop the time out
      if format_time(msg_time) == None:
        await client.send_message(message.channel, 'Make sure the start time you have provided is in the format of [num][s/m/h/d][num][s/m/h/d] etc. with no spaces, eg. 10s for 10 seconds or 10s12m15h1d for 10 seconds, 12 minutes, 15 hours and 1 day.')
        return
      else:
        reminder_time = str(format_time(msg_time))

      msg_interval = text.pop(0) ## pop the interval length out

      interval = format_time(msg_interval)
      if interval == None:
        await client.send_message(message.channel, 'Make sure the interval frequency you have provided is in the format of [num][s/m/h/d][num][s/m/h/d] etc. with no spaces, eg. 10s for 10 seconds or 10s12m15h1d for 10 seconds, 12 minutes, 15 hours and 1 day.')
        return
      else:
        reminder_interval = str(int(round(interval - time.time())))
        if int(reminder_interval) < 10:
          await client.send_message(message.channel, 'That interval is a bit short. For server and sanity reasons, please make your interval longer than 10 seconds.')
          return

      msg_author = message.channel

      msg_text = ' '.join(text)

      intervals.append([reminder_time,reminder_interval,msg_author.id,msg_text])

      await client.send_message(message.channel, 'New interval registered for ' + msg_author.mention + ' in ' + str(int(reminder_time) - int(time.time())) + ' seconds . You can\'t edit the interval now, so you are free to delete the message.')
      print('Registered a new interval for ' + msg_author.name)
  else:
    await client.send_message(message.channel, 'You need to be a Patron (donating 2$ or more) to access this command! Type `$donate` to find out more.')
