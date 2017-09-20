import discord
import asyncio
from globalvars import *


async def accept_invite(message):
  msg = message.content.strip().split(' ')
  msg.pop(0)

  msg = ''.join(msg)

  try:
    await client.accept_invite(msg)
    await client.send_message(message.channel, 'Success!')

  except Exception as e:
    await client.send_message(message.channel, 'Hmm... ' + str(e) + ' went wrong... make sure you provide the invite as a correct URL (http://discord.gg/invitecodehere)')
