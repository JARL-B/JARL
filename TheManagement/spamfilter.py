import json

from TheManagement.globalvars import spam_filter

async def spamfilter(message,client):
  if not message.author.server_permissions.administrator:
    await client.send_message(message.channel, 'You must be an admin to run this command.')
    return
    
  if message.channel.id in spam_filter:
    spam_filter.remove(message.channel.id)
    await client.send_message(message.channel, 'Turned off spam filtering for ' + message.channel.mention)
  else:
    spam_filter.append(message.channel.id)
    await client.send_message(message.channel, 'Spam filtering has been enabled for ' + message.channel.mention)

  with open('DATA/spamfilter.json','w') as f:
    json.dump(spam_filter,f)
