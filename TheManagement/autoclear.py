import discord
import asyncio
import json

from TheManagement.globalvars import autoclears

async def autoclear(message,client):
  if not message.author.guild_permissions.administrator:
    await message.channel.send('You must be an admin to run this command.')
    return

  seconds = 10

  for item in message.content.split(' '): # determin a seconds argument
    try:
      seconds = float(item)
      break
    except ValueError:
      continue

  if len(message.channel_mentions) == 0:
    if message.channel.id in autoclears.keys():
      del autoclears[message.channel.id]
      await message.channel.send(embed=discord.Embed(description='Autoclearing disabled on {}'.format(message.channel.mention)))
    else:
      autoclears[message.channel.id] = seconds
      await message.channel.send(embed=discord.Embed(description='{} second autoclearing enabled on {}'.format(seconds, message.channel.mention)))

  else:
    disable_all = True
    for i in message.channel_mentions:
      if i.id not in autoclears.keys():
        disable_all = False
      autoclears[i.id] = seconds


    if disable_all:
      for i in message.channel_mentions:
        del autoclears[i.id]

      await message.channel.send(embed=discord.Embed(description='Autoclearing disabled on multiple channels'))
    else:
      await message.channel.send(embed=discord.Embed(description='{} second autoclearing enabled on specified channels'.format(seconds)))

  with open('DATA/autoclears.json','w') as f:
    json.dump(autoclears,f)
