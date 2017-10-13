import discord
import json

from TheManagement.globalvars import verif_servers

async def verification(message,client):
  if not message.author.server_permissions.administrator:
    await client.send_message(message.channel, 'You must be an admin to run this command.')
    return

  if discord.utils.get(message.server.roles, name='Manager:Email Verified') == None:
    await client.create_role(message.server, name='Manager:Email Verified')

  if message.server.id in verif_servers:
    await client.send_message(message.channel, 'Custom email verification disabled for this server')
    verif_servers.remove(message.server.id)
  else:
    await client.send_message(message.channel, 'Custom email verification enabled for this server. New members will be asked for email verification.')
    verif_servers.append(message.server.id)

  with open('DATA/verif_servers.json','w') as f:
    json.dump(verif_servers,f)
