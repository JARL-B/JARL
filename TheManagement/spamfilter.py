import json

from TheManagement.globalvars import spam_filter

async def spamfilter(message,client):
  if not message.author.guild_permissions.administrator:
    await message.channel.send('You must be an admin to run this command.')
    return

  if message.channel.id in spam_filter:
    spam_filter.remove(message.channel.id)
    await message.channel.send('Turned off spam filtering for ' + message.channel.mention)
  else:
    spam_filter.append(message.channel.id)
    await message.channel.send('Spam filtering has been enabled for ' + message.channel.mention)

  with open('DATA/spamfilter.json','w') as f:
    json.dump(spam_filter,f)
