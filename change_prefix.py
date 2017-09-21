import discord
import asyncio
from globalvars import *


async def change_prefix(message):
  text = message.content.strip().split(' ')
  text.pop(0)
  text = ' '.join(text)

  if 0 < len(text) < 5:
    prefix[message.server.id] = text
    print(prefix)
    await client.send_message(message.channel, 'Prefix has been set to \'' + text + '\' for this server.')

    with open('DATA/prefix.json','w') as f:
      json.dump(prefix,f)
