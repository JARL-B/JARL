import discord
import asyncio
from globalvars import *
import time
import json
from itertools import chain
import random

from get_patrons import get_patrons


async def check_reminders():
  await client.wait_until_ready()
  while not client.is_closed():

    for reminder in calendar:
      if len(reminder.message) > 400:
        calendar.remove(reminder)

      if reminder.time <= time.time():
        users = client.get_all_members()
        channels = client.get_all_channels()

        msg_points = chain(users, channels)

        recipient = discord.utils.get(msg_points, id=reminder.channel)

        try:
          await recipient.send(reminder.message)
          print('Administered reminder to ' + recipient.name)

        except:
          print('Couldn\'t find required channel. Skipping a reminder')

        calendar.remove(reminder)

    for inv in intervals:
      if inv.time <= time.time():
        channels = client.get_all_channels()
        users = client.get_all_members()

        msg_points = chain(users, channels)

        recipient = discord.utils.get(msg_points, id=inv.channel)

        try:
          server_members = recipient.guild.members
          patrons = get_patrons('Donor')

          for m in server_members:
            if m in patrons:
              if inv.message.startswith('-del_on_send'):
                try:
                  await recipient.purge(check=lambda m: m.content == inv[3][12:].strip() and time.time() - m.created_at.timestamp() < 1209600 and m.author == client.user)
                except Exception as e:
                  print(e)

                await recipient.send(inv[3][12:])

              elif inv.message.startswith('getfrom['):
                id_started = False
                chars = ''
                for char in inv.message[8:].strip():
                  if char in '0123456789':
                    id_started = True
                    chars += char
                  elif id_started:
                    break

                channel_id = int(chars)
                get_from = [s for s in recipient.guild.channels if s.id == channel_id]
                if not get_from:
                  print('getfrom call failed')
                  intervals.remove(inv)
                  continue

                a = []
                async for item in get_from[0].history(limit=50):
                  a.append(item)
                quote = random.choice(a)

                await recipient.send(quote.content)

              else:
                await recipient.send(inv.message)
              print('Administered interval to ' + recipient.name)
              break
          else:
            await recipient.send('There appears to be no patrons on your server, so the interval has been removed.')
            intervals.remove(inv)

          print(inv)
          inv.time += inv.interval ## change the time for the next interval
        except Exception as e:
          print(e)
          print('Couldn\'t find required channel. Skipping an interval')
          intervals.remove(inv)


    with open('DATA/calendar.json','w') as f:
      json.dump([r.__dict__ for r in calendar], f) ## uses a JSON writer to write the data to file.

    with open('DATA/intervals.json','w') as f:
      json.dump([r.__dict__ for r in intervals], f) ## uses a JSON writer to write the data to file.

    await asyncio.sleep(2.5)
