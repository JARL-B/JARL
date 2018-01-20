import discord
import asyncio
from globalvars import *


async def change_prefix(message):
  if not message.author.guild_permissions.administrator:
    await message.channel.send('You must be an admin to run this command.')
    return

  text = message.content.strip().split(' ')
  text.pop(0)
  text = ' '.join(text)

  if 0 < len(text) < 5:
    prefix[message.guild.id] = text
    print(prefix)
    await message.channel.send('Prefix has been set to \'' + text + '\' for this server.')

    with open('DATA/prefix.json','w') as f:
      json.dump(prefix, f)

  else:
    try:
      current_pref = prefix[message.guild.id]
    except KeyError:
      current_pref = '$'

    await message.channel.send('Please make sure your prefix is between 1 and 5 characters. Your current prefix is {}'.format(current_pref))
