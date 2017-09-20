import discord
import asyncio

from globalvars import *

def validate_event(message,loc):
  if loc == 'server':
    li = [ch.id for ch in message.server.channels]

    reminders = [r for r in calendar if r[1] in li]

    if len(reminders) > 8:
      return False

    return True

  elif loc == 'me':
    reminders = [r for r in calendar if r[1] == message.author]

    if len(reminders) > 6:
      return False

    return True
