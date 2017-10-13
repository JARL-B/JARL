import json

from TheManagement.globalvars import profanity_filter

async def profanityfilter(message,client):
  if not message.author.server_permissions.administrator:
    await client.send_message(message.channel, 'You must be an admin to run this command.')
    return
    
  if message.channel.id in profanity_filter:
    profanity_filter.remove(message.channel.id)
    await client.send_message(message.channel, 'Turned off profanity filtering for ' + message.channel.mention)
  else:
    profanity_filter.append(message.channel.id)
    await client.send_message(message.channel, 'Profanity filtering has been enabled for ' + message.channel.mention)

  with open('DATA/profanityfilter.json','w') as f:
    json.dump(profanity_filter,f)
