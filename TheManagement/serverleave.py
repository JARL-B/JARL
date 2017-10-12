import json

from TheManagement.globalvars import leave_messages

async def serverleave(message,client):
  if message.server.id in leave_messages.keys():
    if len(message.content.split(' ')) == 1:
      await client.send_message(message.channel, 'Server leave messages disabled!')
      del leave_messages[message.server.id]
    else:
      leave_messages[message.server.id] = [message.content.split(' ',1)[1], message.channel.id]
  else:
    if len(message.content.split(' ')) == 1:
      await client.send_message(message.channel, 'It appears your server doesn\'t yet have a leave message! To set one, type this command followed by a space, followed by your message. Use two curly braces (`{}`) to represent the name of the person who left (we\'ll replace them automatically)')
    else:
      leave_messages[message.server.id] = [message.content.split(' ',1)[1], message.channel.id]

  with open('DATA/leave_messages.json','w') as f:
    json.dump(leave_messages,f)
