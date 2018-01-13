from TheManagement.globalvars import terms
from get_patrons import get_patrons
import json

async def term_blacklist(message, client):
  if message.author not in get_patrons('Donor'):
    await client.send_message(message.channel, 'You must be a patron (donating $2 or more) to use this command!')
    return

  if not message.author.server_permissions.administrator:
    await client.send_message(message.channel, 'You must be an admin to run this command.')
    return

  if message.server.id in terms.keys() and terms[message.server.id]['enabled']:
    contents = message.content.split(' ', 1)
    if len(contents) == 1:
      terms[message.server.id]['enabled'] = False
      await client.send_message(message.channel, 'Term filtering has been disabled.')

    else:
      if contents[-1] == 'show':
        await client.send_message(message.channel, 'Terms being filtered: ' + ', '.join(terms[message.server.id]['filters']))
        return
        
      for term in contents[-1].split(','):
        if len(''.join(terms[message.server.id]['filters'])) > 200:
          client.send_message(message.channel, 'Character limit for server filter reached. Try and reduce the number of filters you have.')
          break

        if term in terms[message.server.id]['filters']:
          terms[message.server.id]['filters'].remove(term)
          await client.send_message(message.channel, 'Removed term `{}`'.format(term))
        else:
          terms[message.server.id]['filters'].append(term)
          await client.send_message(message.channel, 'Added term `{}`'.format(term))

  else:
    terms[message.server.id] = {'enabled' : True, 'filters' : []}
    await client.send_message(message.channel, 'Term filtering has been enabled. Please use the command followed by a word to add the word to filtering.')

  with open('DATA/terms.json','w') as f:
    json.dump(terms, f)
