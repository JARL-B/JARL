import json

from TheManagement.globalvars import join_messages

async def serverjoin(message,client):
  if not message.author.guild_permissions.administrator:
    await message.channel.send('You must be an admin to run this command.')
    return

  if message.guild.id in join_messages.keys():
    if len(message.content.split(' ')) == 1:
      await message.channel.send('Server join messages disabled!')
      del join_messages[message.guild.id]
    else:
      join_messages[message.guild.id] = [message.content.split(' ',1)[1], message.channel.id]
      await message.channel.send('Server join messages enabled!')

  else:
    if len(message.content.split(' ')) == 1:
      await message.channel.send('It appears your server doesn\'t yet have a join message! To set one, type this command followed by a space, followed by your message. Use two curly braces (`{}`) to represent the name of the person who joined (we\'ll replace them automatically)')
    else:
      join_messages[message.guild.id] = [message.content.split(' ',1)[1], message.channel.id]
      await message.channel.send('Server join messages enabled!')


  with open('DATA/join_messages.json', 'w') as f:
    json.dump(join_messages, f)
