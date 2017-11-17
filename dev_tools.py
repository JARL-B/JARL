import asyncio
import discord

from globalvars import *
from get_patrons import get_patrons

async def dev_tools(message,client):
  command = message.content.split(' ').pop(1)

  if command == 'roles':
    roles = message.server.roles
    prts = []
    for r in roles:
      prts.append('{}, {}\n'.format(r.id, r.name))

    await client.send_message(message.channel, ''.join(prts))

  elif command == 'serverid':
    await client.send_message(message.channel, message.server.id)

  elif command == 'channelid':
    await client.send_message(message.channel, message.channel.id)

  elif command == 'patrons':
    li = [i.name for i in get_patrons()]
    await client.send_message(message.channel, ' '.join(li))

  elif command == 'donors':
    li = [i.name for i in get_patrons('Donors')]
    await client.send_message(message.channel, ' '.join(li))

  elif command == 'upatrons':
    li = [i.name for i in get_patrons('Ultra-Patrons')]
    await client.send_message(message.channel, ' '.join(li))

  elif command == 'servers':
    await client.send_message(message.channel, len(client.servers))

  elif command == 'n_cal':
    await client.send_message(message.channel, len(calendar))

  else:
    await client.send_message(message.channel, 'Hello! You\'ve found the dev options. Commands are `roles`, `serverid`, `channelid` and `patrons`')
