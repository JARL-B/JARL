from TheManagement.globalvars import emails

async def get_emails(message,client):
  if not message.author.server_permissions.administrator:
    await client.send_message(message.channel, 'You must be an admin to run this command.')
    return
    
  printli = []
  for member in message.server.members:
    try:
      printli.append('User {} ({})'.format(member.name,emails[member.id]))
    except KeyError:
      printli.append('No email for user {}'.format(member.name))

  strings = [', '.join(printli[i:i+12]) for i in range(0,len(printli),12)]

  for s in strings:
    await client.send_message(message.author, s)
