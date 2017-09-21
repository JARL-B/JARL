from TheManagement.globalvars import profanity_filter

async def profanityfilter(message,client):
  if message.channel.id in profanity_filter:
    profanity_filter.remove(message.channel.id)
    await client.send_message(message.channel, 'Turned off profanity filtering for ' + message.channel.mention)
  else:
    profanity_filter.append(message.channel.id)
    await client.send_message(message.channel, 'Profanity filtering has been enabled for ' + message.channel.mention)

  with open('DATA/profanityfilter','w') as f:
    bl_s = ''
    for i in profanity_filter:
      bl_s += i + ','

    f.write(bl_s)
