import discord
import time
import asyncio

from RemindMe.validate_event import validate_event
from RemindMe.format_time import format_time
from RemindMe.globalvars import calendar

from get_patrons import get_patrons

async def set_reminder(message, client):
  if ',' in message.content or ';' in message.content:
    await client.send_message(message.channel, 'Sorry, but you cannot place commas or semi-colons inside your reminders due to storage formats')
  else:
    text = message.content.split(' ')
    text.pop(0) ## remove the command item

    msg_scope = text.pop(0).replace('#','')
    try:
      if msg_scope not in [c.name for c in message.server.channels if c.type == discord.ChannelType.text] + ['server', 'me'] and client.get_channel(msg_scope[1:-1]).server != message.server:
        await client.send_message(message.channel, 'You must specify either `server`, `me` or a channel name for your reminder! `me` will be sent directly to you, whilst `server` will be broadcasted on the current text channel.')
        return
    except AttributeError:
      await client.send_message(message.channel, 'You must specify either `server`, `me` or a channel name for your reminder! `me` will be sent directly to you, whilst `server` will be broadcasted on the current text channel.')
      return

    if not validate_event(message,msg_scope) and message.author not in get_patrons(level='Patrons'):
      await client.send_message(message.channel, 'Sorry, but you have reached the limit of pending reminders. Please note that the server limit is 8 reminders active max and the personal limit is 6 max. You can use `$del` to delete reminders, donate to me on Patreon using `$donate` or blacklist channels to prevent buildup of reminders using `$blacklist`.')
      return

    msg_time = text.pop(0) ## pop the time out
    if format_time(msg_time) == None:
      await client.send_message(message.channel, 'Make sure the time you have provided is in the format of [num][s/m/h/d][num][s/m/h/d] etc. with no spaces, eg. 10s for 10 seconds or 10s12m15h1d for 10 seconds, 12 minutes, 15 hours and 1 day.')
      return
    else:
      reminder_time = str(format_time(msg_time))

    if msg_scope == 'server':
      msg_author = message.channel
    elif msg_scope == 'me':
      msg_author = message.author
    elif msg_scope[0] == '<':
      msg_author = client.get_channel(msg_scope[1:-1])
    else:
      msg_author = [c for c in message.server.channels if c.name == msg_scope][0]
    msg_text = ' '.join(text)

    if len(msg_text) > 150 and message.author not in get_patrons(level='Donor'):
      await client.send_message(message.channel, 'You are allowed a maximum of 150 characters in your reminder text (you used {}). Either reduce your message size, or `$donate`.'.format(len(msg_text)))
      return

    calendar.append([reminder_time,msg_author.id,msg_text])

    await client.send_message(message.channel, 'New reminder registered for ' + msg_author.mention + ' in ' + str(int(reminder_time) - int(time.time())) + ' seconds . You can\'t edit the reminder now, so you are free to delete the message.')
    print('Registered a new reminder for ' + msg_author.name)
