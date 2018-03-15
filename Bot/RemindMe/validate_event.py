import discord
import asyncio

from globalvars import *

def count_reminders(loc):
    return len([r for r in reminders.queue if r.channel == loc and r.interval == None])
