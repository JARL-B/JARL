from globalvars import *
import asyncio
import discord

async def add_blacklist(message,client):
  if not message.author.guild_permissions.administrator:
    await message.channel.send('You must be an admin to run this command.')
    return

  text = message.content.strip().split(' ')

  if len(text) > 1:
    text.pop(0)
    text = ' '.join(text)

    text = text.replace('#','')
    channel = discord.utils.get(client.get_all_channels(),name=text, guild=message.guild)

  else:
    channel = message.channel

  if channel == None:
    await message.channel.send('Couldn\'t find a channel matching your keywords.')
    return

  if channel.id in channel_blacklist:
    channel_blacklist.remove(channel.id)
    await message.channel.send('Removed ' + channel.mention + ' from the blacklist')

  else:
    channel_blacklist.append(channel.id)
    await message.channel.send('Added ' + channel.mention + ' to the blacklist.')

  with open('DATA/blacklist.json','w') as f:
    json.dump(channel_blacklist,f)
