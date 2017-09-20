from globalvars import *
from get_patrons import get_patrons

async def bind(message):
  if message.author in get_patrons('Ultra-Patrons'):
    try:
      if len(binds[message.author.id]) < 3:
        binds[message.author.id].append(message.server.id)

      else:
        binds[message.server.id].pop(0)
        binds[message.author.id].append(message.server.id)

    except KeyError:
      binds[message.author.id] = [message.server.id]

  elif message.author in get_patrons('Patrons'):
    binds[message.author.id] = [message.server.id]

  else:
    await client.send_message(message.channel, 'You need to be a Patron (donating 5$ or more) to access this command! Type `$donate` to find out more.')
