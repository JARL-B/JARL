from globalvars import *
import asyncio
import discord

async def add_blacklist(message):
  text = message.content.strip().split(' ')
  text.pop(0)
  text = ' '.join(text)

  text = text.replace('#','')
  channel = discord.utils.get(client.get_all_channels(),name=text,server=message.server)

  if channel == None:
    await client.send_message(message.channel, 'Couldn\'t find a channel matching your keywords.')
    return

  elif channel == message.channel:
    await client.send_message(message.channel, 'You can\'t block your current channel from sending messages. Try again from another channel.')
    return

  if channel.id in channel_blacklist:
    channel_blacklist.remove(channel.id)
    await client.send_message(message.channel, 'Removed ' + channel.mention + ' from the blacklist')

  else:
    channel_blacklist.append(channel.id)
    await client.send_message(message.channel, 'Added ' + channel.mention + ' to the blacklist.')
