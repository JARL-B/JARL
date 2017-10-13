import discord
import json

from TheManagement.globalvars import tag_filter

async def tagfilter(message,client):
  if not message.author.server_permissions.administrator:
    await client.send_message(message.channel, 'You must be an admin to run this command.')
    return

  if discord.utils.get(message.server.roles, name='Manager:Allow @here') == None:
    await client.create_role(message.server, name='Manager:Allow @here')

  if message.channel.id in tag_filter:
    tag_filter.remove(message.channel.id)
    await client.send_message(message.channel, 'Turned off tag filtering for ' + message.channel.mention)
  else:
    tag_filter.append(message.channel.id)
    await client.send_message(message.channel, 'Tag filtering has been enabled for ' + message.channel.mention)

  with open('DATA/tag_filter.json','w') as f:
    json.dump(tag_filter,f)
