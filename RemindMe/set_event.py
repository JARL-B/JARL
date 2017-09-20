import discord
import time
import asyncio
import datetime

from globalvars import *
from validate_event import validate_event
from get_binds import get_binds

async def set_event(message, client):
  if ',' in message.content or ';' in message.content:
    await client.send_message(message.channel, 'Sorry, but you cannot place commas or semi-colons inside your events due to storage formats')
  else:
    text = message.content.split(' ')
    text.pop(0) ## remove the command item

    msg_scope = text.pop(0)
    if not msg_scope in ['server','me']:
      await client.send_message(message.channel, 'You must specify either `server` or `me` for your reminder! `me` will be sent directly to you, whilst `server` will be broadcasted on the current text channel.')
      return

    if not (validate_event(message,msg_scope) and (message.author in get_patrons(level='Patrons') or message.server in get_binds())):
      await client.send_message(message.channel, 'Sorry, but you have reached the limit of pending reminders. Please note that the server limit is 8 reminders active max and the personal limit is 6 max. You can use `$del` to delete reminders, donate to me on Patreon using `$donate` or blacklist channels to prevent buildup of reminders using `$blacklist`.')
      return

    if msg_scope == 'server':
      msg_author = message.channel
    elif msg_scope == 'me':
      msg_author = message.author

    msg_time = text.pop(0) ## pop the time out

    current_buffer = ''
    minutes = '0'
    hours = '0'
    days = '1'
    months = '1'
    year = '2018'

    for char in msg_time:

      if char == 'm':
        minutes = current_buffer
        current_buffer = ''

      elif char == 'h':
        hours = current_buffer
        current_buffer = ''

      elif char == 'd':
        days = current_buffer
        current_buffer = ''

      elif char == '/':
        months = current_buffer
        current_buffer = ''

      elif char == 'y':
        year = current_buffer
        current_buffer = ''

      elif char == ' ':
        continue

      else:
        try:
          int(char)
          current_buffer += char
        except ValueError:
          await client.send_message(message.channel, 'Make sure the date you have provided is in the format of [num]m[num]h[num]d[num]/[num]y with no spaces, eg. 00:00 on the 31st of December 2020 would be 0m0m31d12/2020y')
          return

    date = minutes + '/' + hours + '/' + days + '/' + months + '/' + year
    try:
      reminder_time = int(round(time.mktime(datetime.datetime.strptime(date, '%M/%H/%d/%m/%Y').timetuple())))
    except ValueError:
      await client.send_message(message.channel, 'Something went wrong. Please make sure you entered only valid numbers for the times and dates.')

    msg_text = ' '.join(text)

    calendar.append([reminder_time,msg_author.id,msg_text])

    await client.send_message(message.channel, 'New event registered for ' + msg_author.mention + ' in ' + str(int(reminder_time) - int(time.time())) + ' seconds . You can\'t edit the reminder now, so you are free to delete the message.')
    print('Registered a new event for ' + msg_author.name)
