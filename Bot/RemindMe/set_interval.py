import discord
import asyncio
import time

from RemindMe.format_time import format_time
from RemindMe.globalvars import reminders
from RemindMe.Reminder import Reminder

from globalvars import restrictions

from get_patrons import get_patrons

async def set_interval(message, client):
    if isinstance(message.channel, discord.DMChannel):
        await message.channel.send('Please use this in a server for now. Functionality will be ported in the future, but for now use your mention as the interval\'s destination')
        return

    if message.author not in get_patrons('Donor'):
        await message.channel.send(embed=discord.Embed(description='You need to be a Patron (donating 2$ or more) to access this command! Type `$donate` to find out more.'))
        return

    args = message.content.split(' ')
    args.pop(0) # remove the command item

    if len(args) < 3:
        await message.channel.send(embed=discord.Embed(title='interval', description='**Usage** ```$interval [channel mention or user mention] <time to or time at> <interval> <message>```\n\n**Example** ```$interval #general 9:30 1d Good morning!``` ```$interval 0s 10s This will be really irritating```'))
        return

    scope = message.channel.id
    pref = '#'

    if args[0].startswith('<'): # if a scope is provided
        if args[0][2:-1][0] == '!':
            tag = int(args[0][3:-1])

        else:
            try:
                tag = int(args[0][2:-1])
            except ValueError:
                await message.channel.send(embed=discord.Embed(description='Please ensure your tag links directly to a user or channel, not a role.'))

        if args[0][1] == '@': # if the scope is a user
            pref = '@'
            scope = message.guild.get_member(tag)

        else:
            pref = '#'
            scope = message.guild.get_channel(tag)

        if scope == None:
            await message.channel.send(embed=discord.Embed(description='Couldn\'t find a location by your tag present.'))
            return

        else:
            scope = scope.id

        args.pop(0)

    msg_time = format_time(args[0], message.guild.id)

    if msg_time == None:
        await message.channel.send(embed=discord.Embed(description='Make sure the time you have provided is in the format of [num][s/m/h/d][num][s/m/h/d] etc. or `day`/`month`/`year`-`hour`:`minute`:`second`.'))
        return

    args.pop(0)

    msg_interval = format_time(args[0], message.guild.id)

    if msg_interval == None:
        await message.channel.send(embed=discord.Embed(description='Make sure the interval you have provided is in the format of [num][s/m/h/d][num][s/m/h/d] etc. with no spaces, eg. 10s for 10 seconds or 10s12m15h1d for 10 seconds, 12 minutes, 15 hours and 1 day.'))
        return

    msg_interval -= time.time()
    msg_interval = round(msg_interval)

    if msg_interval < 8:
        await message.channel.send(embed=discord.Embed(description='Please make sure your interval timer is longer than 8 seconds.'))
        return

    args.pop(0)

    msg_text = ' '.join(args)

    if len(msg_text) > 150 and message.author not in get_patrons('Patrons'):
        await message.channel.send(embed=discord.Embed(description='Interval message too long! (max 150, you used {}). Use `$donate` to increase your character limit to 1900 ($5 tier)'.format(len(msg_text))))
        return

    if len(msg_text) >= 1900:
        await message.channel.send(embed=discord.Embed(description='Discord restrictions mean we can\'t send reminders 2000+ characters. Sorry'))
        return

    if pref == '#':
        if not message.author.guild_permissions.manage_messages:
            if scope not in restrictions.keys():
                restrictions[scope] = []
            for role in message.author.roles:
                if role.id in restrictions[scope]:
                    break
            else:
                await message.channel.send(embed=discord.Embed(description='You must be either admin or have a role capable of sending reminders to that channel. Please talk to your server admin, and tell her/him to use the `$restrict` command to specify allowed roles.'))
                return

    reminders.append(Reminder(time=msg_time, interval=msg_interval, channel=scope, message=msg_text))
    reminders.sort(key=lambda x: x.time)

    await message.channel.send(embed=discord.Embed(description='New interval registered for <{}{}> in {} seconds . You can\'t edit the reminder now, so you are free to delete the message.'.format(pref, scope, round(msg_time - time.time()))))
    print('Registered a new interval for {}'.format(message.guild.name))
