from globalvars import *
import asyncio
import discord

async def add_blacklist(message,client):
  if not message.author.guild_permissions.administrator:
    await message.channel.send('You must be an admin to run this command.')
    return

  if len(message.channel_mentions) > 0:
    disengage_all = True

    for mention in message.channel_mentions:
      if mention.id not in channel_blacklist:
        disengage_all = False

    if disengage_all:
      for mention in message.channel_mentions:
        channel_blacklist.remove(mention.id)

      await message.channel.send(embed=discord.Embed(description='Removed blacklists from specified channels'))

    else:
      for mention in message.channel_mentions:
        if mention.id not in channel_blacklist:
          channel_blacklist.append(mention.id)

      await message.channel.send(embed=discord.Embed(description='Blacklisted specified channels'))

  else:
    if message.channel.id in channel_blacklist:
      channel_blacklist.remove(message.channel.id)
      await message.channel.send(embed=discord.Embed(description='Removed blacklist from current channel'))

    else:
      channel_blacklist.append(message.channel.id)
      await message.channel.send(embed=discord.Embed(description='Blacklisted current channel'))


  with open('DATA/blacklist.json','w') as f:
    json.dump(channel_blacklist,f)
