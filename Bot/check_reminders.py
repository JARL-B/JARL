import discord
import asyncio
from globalvars import *
import time
from itertools import chain
import random
import datetime
import sqlite3

from get_patrons import get_patrons


async def check_reminders():
    await client.wait_until_ready()

    times['start'] = time.time()
    while not client.is_closed():
        times['last_loop'] = time.time()
        times['loops'] += 1

        while len(reminders.queue) and reminders.queue[0].time <= time.time():
            print('Looping for reminder(s)...')

            reminder = reminders.get()

            if reminder.delete:
                print('{}: Deleted reminder'.format(datetime.datetime.utcnow().strftime('%H:%M:%S')))
                continue

            users = client.get_all_members()
            channels = client.get_all_channels()

            msg_points = chain(users, channels)

            recipient = discord.utils.get(msg_points, id=reminder.channel)

            if recipient == None:
                print('{}: Failed to locate channel'.format(datetime.datetime.utcnow().strftime('%H:%M:%S')))
                continue

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
                        continue

                    while reminder.time < time.time():
                        if reminder.interval < 8:
                            continue
                        reminder.time += reminder.interval ## change the time for the next interval
                    reminders.put(reminder) # Requeue the interval with modified time

            except Exception as e:
                print(e)

        cursor.execute('DELETE FROM reminders')
        cursor.execute('VACUUM')

        for d in map(lambda x: x.__dict__, reminders.queue):
            if d['delete']:
                continue

            command = '''INSERT INTO reminders (interval, time, channel, message)
            VALUES (?, ?, ?, ?)'''

            cursor.execute(command, (d['interval'], d['time'], d['channel'], d['message']))

        connection.commit()

        await asyncio.sleep(2.5)