import json

from TheManagement.globalvars import join_messages

async def serverjoin(message,client):
  if not message.author.server_permissions.administrator:
    await client.send_message(message.channel, 'You must be an admin to run this command.')
    return

  if message.server.id in join_messages.keys():
    if len(message.content.split(' ')) == 1:
      await client.send_message(message.channel, 'Server join messages disabled!')
      del join_messages[message.server.id]
    else:
      join_messages[message.server.id] = [message.content.split(' ',1)[1], message.channel.id]
  else:
    if len(message.content.split(' ')) == 1:
      await client.send_message(message.channel, 'It appears your server doesn\'t yet have a join message! To set one, type this command followed by a space, followed by your message. Use two curly braces (`{}`) to represent the name of the person who joined (we\'ll replace them automatically)')
    else:
      join_messages[message.server.id] = [message.content.split(' ',1)[1], message.channel.id]

  with open('DATA/join_messages.json','w') as f:
    json.dump(join_messages,f)
