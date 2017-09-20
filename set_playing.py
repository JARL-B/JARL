import asyncio
import discord
import re
import uuid

from globalvars import *
from get_patrons import get_patrons


async def set_playing(message):
  if message.author in get_patrons(level='Donor'):
    msg = message.content.split(' ')
    msg.pop(0) ## remove the command text
    uid = str(uuid.uuid4())

    msg = ' '.join(msg)

    compressed = ''.join(msg) ## remove all spaces

    with open('profanity','r') as f:
      for reg in f:
        reg = reg.strip()
        exp = re.search(reg,compressed)
        if exp: ## perform a regex search for illicit terms
          with open('warnings','a') as f2:
            f2.write(exp.group() + ' term detected at ' + message.author.name + ' (UUID ' + uid + ')')
          print(exp.group() + ' term detected at ' + message.author.name + ' (UUID ' + uid + ')')
          await client.send_message(message.channel, 'Illicit term \'{}\' detected in input. You have been warned... (if you believe this warning has been administered wrongly, please send the code {} to the support channel in the Discord group)'.format(exp.group(),uid))
          return
      else:
        print(msg + ' term sent to bot playing at ' + message.author.name + ':' + message.author.id)
        await client.change_presence(game=discord.Game(name=msg))

  else:
    await client.send_message(message.channel, 'You must be a Patron (donating 2$ or more) to access this command!')
