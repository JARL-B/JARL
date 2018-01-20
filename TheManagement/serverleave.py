import json

from TheManagement.globalvars import leave_messages

async def serverleave(message,client):
  if not message.author.guild_permissions.administrator:
    await message.channel.send('You must be an admin to run this command.')
    return

  if message.guild.id in leave_messages.keys():
    if len(message.content.split(' ')) == 1:
      await message.channel.send('Server leave messages disabled!')
      del leave_messages[message.guild.id]
    else:
      leave_messages[message.guild.id] = [message.content.split(' ',1)[1], message.channel.id]
      await message.channel.send('Server leave messages enabled!')

  else:
    if len(message.content.split(' ')) == 1:
      await message.channel.send('It appears your server doesn\'t yet have a leave message! To set one, type this command followed by a space, followed by your message. Use two curly braces (`{}`) to represent the name of the person who left (we\'ll replace them automatically)')
    else:
      leave_messages[message.guild.id] = [message.content.split(' ',1)[1], message.channel.id]
      await message.channel.send('Server leave messages enabled!')


  with open('DATA/leave_messages.json','w') as f:
    json.dump(leave_messages,f)
