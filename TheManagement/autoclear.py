import discord
import asyncio
import json

from TheManagement.globalvars import autoclears


async def autoclear(message,client):
  if not message.author.server_permissions.administrator:
    await client.send_message(message.channel, 'You must be an admin to run this command.')
    return

  text = message.content.strip(' ').split(' ')
  text.pop(0)

  if len(text) == 0:
    if message.channel.id in autoclears.keys():
      del autoclears[message.channel.id]
      await client.send_message(message.channel, 'Autoclearing disabled for this channel.')

      return

    autoclears[message.channel.id] = 10
    await client.send_message(message.channel, '10 second autoclearing has been enabled for this channel.')

  elif len(text) == 1:
    try:
      seconds = float(text[0])
      autoclears[message.channel.id] = seconds
      await client.send_message(message.channel, str(seconds) + ' second autoclearing has been enabled for this channel')

    except ValueError:
      channel = discord.utils.get(client.get_all_channels(),name=text[0],server=message.server)
      if channel != None:
        autoclears[channel.id] = 10
        await client.send_message(message.channel, '10 second autoclearing has been enabled for ' + channel.mention())
      else:
        await client.send_message(message.channel, 'Couldn\'t find channel specified. Please type just the channel name (don\'t mention it!)')

  elif len(text) == 2:
    try:
      seconds = float(text[0])
      channel = discord.utils.get(client.get_all_channels(),name=text[1],server=message.server)
      if channel != None:
        autoclears[channel.id] = seconds
        await client.send_message(message.channel, str(seconds) + ' second autoclearing has been enabled for ' + channel.mention)

      else:
        await client.send_message(message.channel, 'Couldn\'t find channel specified. Please type just the channel name (don\'t mention it!)')

    except ValueError:
      try:
        seconds = float(text[1])
        channel = discord.utils.get(client.get_all_channels(),name=text[0],server=message.server)
        if channel != None:
          autoclears[channel.id] = seconds
          await client.send_message(message.channel, str(seconds) + ' second autoclearing has been enabled for ' + channel.mention)

        else:
          await client.send_message(message.channel, 'Couldn\'t find channel specified. Please type just the channel name (don\'t mention it!)')

      except ValueError:
        await client.send_message(message.channel, 'Please ensure your parameters consist of a decimal time and the name (not the mention) of the text channel.')

  else:
    await client.send_message(message.channel, 'Too many parameters provided. Please provide a clearing timer (a decimal number) and a channel name')

  with open('autoclears.json','w') as f:
    json.dump(autoclears,f)
