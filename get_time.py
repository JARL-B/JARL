from globalvars import *
import time
import asyncio


async def get_time(message):
  await client.send_message(message.channel, 'The time since the epoch in seconds is ' + str(round(time.time())))
