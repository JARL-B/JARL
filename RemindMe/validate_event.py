import discord
import asyncio

from globalvars import *

def count_reminders(loc):
  return len([r for r in calendar if r[1] == loc])
