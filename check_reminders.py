import discord
import asyncio
from globalvars import *
import time
import json
from itertools import chain
import random
import datetime

from get_patrons import get_patrons


async def check_reminders():
    await client.wait_until_ready()
    while not client.is_closed():
        last_loop[0] = time.time()

        reminders.sort(key=lambda x: x.time)

        while len(reminders) and reminders[0].time <= time.time():
            print('Looping for reminder(s)...')

            reminder = reminders.pop(0)

            if reminder.delete:
                print('{}: Deleted reminder'.format(datetime.datetime.utcnow().strftime('%H:%M:%S')))
                continue

            users = client.get_all_members()
            channels = client.get_all_channels()

            msg_points = chain(users, channels)

            recipient = discord.utils.get(msg_points, id=reminder.channel)

            try:
                if reminder.interval == None:
                    await recipient.send(reminder.message)
                    print('{}: Administered reminder to {}'.format(datetime.datetime.utcnow().strftime('%H:%M:%S'), recipient.name))

                else:
                    server_members = recipient.guild.members
                    patrons = get_patrons('Donor')

                    if any([m in patrons for m in server_members]):
                        if reminder.message.startswith('-del_on_send'):
                            try:
                                await recipient.purge(check=lambda m: m.content == reminder.message[12:].strip() and time.time() - m.created_at.timestamp() < 1209600 and m.author == client.user)
                            except Exception as e:
                                print(e)

                            await recipient.send(reminder.message[12:])

                        elif reminder.message.startswith('getfrom['):
                            id_started = False
                            chars = ''
                            for char in reminder.message[8:].strip():
                                if char in '0123456789':
                                    id_started = True
                                    chars += char
                                elif id_started:
                                    break

                            channel_id = int(chars)
                            get_from = [s for s in recipient.guild.channels if s.id == channel_id]
                            if not get_from:
                                print('getfrom call failed')
                                intervals.remove(reminder)
                                continue

                            a = []
                            async for item in get_from[0].history(limit=50):
                                a.append(item)
                            quote = random.choice(a)

                            await recipient.send(quote.content)

                        else:
                            await recipient.send(reminder.message)
                        print('{}: Administered interval to {} (Reset for {} seconds)'.format(datetime.datetime.utcnow().strftime('%H:%M:%S'), recipient.name, reminder.interval))
                    else:
                        await recipient.send('There appears to be no patrons on your server, so the interval has been removed.')
                        return

                    while reminder.time < time.time():
                        if reminder.interval < 8:
                            continue
                        reminder.time += reminder.interval ## change the time for the next interval
                    reminders.append(reminder) # Requeue the interval with modified time

            except Exception as e:
                print(e)
                print('Couldn\'t find required channel. Skipping a reminder')

        with open('DATA/calendar.json', 'w') as f:
            json.dump([r.__dict__ for r in reminders], f) ## uses a JSON writer to write the data to file.

        await asyncio.sleep(2.5)
