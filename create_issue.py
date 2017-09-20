from globalvars import *
import asyncio
import discord
from datetime import datetime


async def create_issue(message):
  msg = message.content.strip().split(' ')
  typ = msg.pop(0)[1:]

  msg = ' '.join(msg)

  if len(msg) == 0:
    await client.send_message(message.channel, 'Please add some words to your issue report.')

  else:
    cti = datetime.now()

    time_str = str(cti.hour) + ':' + str(cti.minute)
    date_str = str(cti.year) + '/' + str(cti.month) + '/' + str(cti.day)

    with open('issues','a') as f:
      f.write(message.author.name + ' filed ' + ('a' if typ=='suggestion' else 'an') + typ + ' at ' + time_str + ' on ' + date_str + ' reading: ' + msg + '\n')

    print(typ.capitalize() + ' registered by ' + message.author.name)

    await client.delete_message(message)
    m = await client.send_message(message.channel, 'Thank you for sending an issue. It has been logged and will be checked as soon as possible.')

    await asyncio.sleep(1.85)
    await client.delete_message(m)
