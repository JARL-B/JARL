import discord
import asyncio
from globalvars import *
import time
import csv
import json
from itertools import chain

from get_patrons import get_patrons


async def check_reminders():
  await client.wait_until_ready()
  while not client.is_closed:
    for reminder in calendar:
      if len(reminder[2]) > 400:
        calendar.remove(reminder)

      if int(reminder[0]) <= time.time():
        users = client.get_all_members()
        channels = client.get_all_channels()

        msg_points = chain(users, channels)

        recipient = discord.utils.get(msg_points,id=reminder[1])

        try:
          await client.send_message(recipient, embed=discord.Embed(description=reminder[2]))
          print('Administered reminder to ' + recipient.name)

        except:
          print('Couldn\'t find required channel. Skipping a reminder')

        calendar.remove(reminder)

    for inv in intervals:
      if int(inv[0]) <= time.time():
        channels = client.get_all_channels()

        recipient = discord.utils.get(channels,id=inv[2])

        try:
          server_members = recipient.server.members
          patrons = get_patrons('Donor')

          for m in server_members:
            if m in patrons:
              if inv[3].startswith('-del_on_send'):
                try:
                  await client.purge_from(recipient, check=lambda m: m.content == inv[3][12:].strip() and time.time() - m.timestamp.timestamp() < 1209600 and m.author == client.user)
                except Exception as e:
                  print(e)

                await client.send_message(recipient, embed=discord.Embed(description=inv[3][12:]))

              else:
                await client.send_message(recipient, inv[3])
              print('Administered interval to ' + recipient.name)
              break
          else:
            await client.send_message(recipient, 'There appears to be no patrons on your server, so the interval has been removed.')
            intervals.remove(inv)

          print(inv)
          inv[0] = str(int(inv[0]) + int(inv[1])) ## change the time for the next interval
        except:
          print('Couldn\'t find required channel. Skipping an interval')
          intervals.remove(inv)


    with open('DATA/calendar.json','w') as f:
      json.dump(calendar, f) ## uses a CSV writer to write the data to file.

    with open('DATA/intervals.json','w') as f:
      json.dump(intervals, f) ## uses a CSV writer to write the data to file.

    await asyncio.sleep(1.5)
