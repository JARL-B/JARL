from globalvars import *
import asyncio
import discord

async def add_blacklist(message,client):
  if not message.author.server_permissions.administrator:
    await client.send_message(message.channel, 'You must be an admin to run this command.')
    return

  text = message.content.strip().split(' ')

  if len(text) > 1:
    text.pop(0)
    text = ' '.join(text)

    text = text.replace('#','')
    channel = discord.utils.get(client.get_all_channels(),name=text,server=message.server)

  else:
    channel = message.channel

  if channel == None:
    await client.send_message(message.channel, 'Couldn\'t find a channel matching your keywords.')
    return

  if channel.id in channel_blacklist:
    channel_blacklist.remove(channel.id)
    await client.send_message(message.channel, 'Removed ' + channel.mention + ' from the blacklist')

  else:
    channel_blacklist.append(channel.id)
    await client.send_message(message.channel, 'Added ' + channel.mention + ' to the blacklist.')

  with open('DATA/blacklist.json','w') as f:
    json.dump(channel_blacklist,f)
