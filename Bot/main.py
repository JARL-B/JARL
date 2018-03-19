import discord
import asyncio
import sys
import os
import time
import aiohttp

from globalvars import *

from RemindMe.set_reminder import set_reminder
from RemindMe.set_interval import set_interval
from RemindMe.del_reminders import del_reminders
from RemindMe.todo import todo
from RemindMe.timezone import timezone

from TheManagement.autoclear import autoclear
from TheManagement.clear_by import clear_by
from TheManagement.spamfilter import spamfilter
from TheManagement.servermsg import servermsg
from TheManagement.tag import tag

from check_reminders import check_reminders
from change_prefix import change_prefix
from add_blacklist import add_blacklist
from donate import donate
from get_help import get_help
from info import info
from ping import ping
from restrict import restrict
from ffs import ffs

from link import link
from unlink import unlink

import server


async def blacklist_msg(message):
    msg = await message.channel.send(embed=discord.Embed(description=':x: This text channel has been blacklisted :x:'))
    await message.delete()
    await asyncio.sleep(2)
    await msg.delete()

async def log(message, client):
    await message.channel.send(embed=discord.Embed(description='\n'.join(['{}: {}'.format(x, y) for x, y in command_log.items()])))

async def timeit(message, client):
    await message.channel.send(embed=discord.Embed(title='timeit', description='Average time over {} loops: {}ms'.format(times['loops'], ((time.time() - times['start'])/times['loops']) * 1000)))

command_map = {
    'help' : get_help,
    'info' : info,
    'remind' : set_reminder,
    'blacklist' : add_blacklist,
    'interval' : set_interval, ## patron only ##
    'del' : del_reminders,
    'donate' : donate,
    'clear' : clear_by,
    'autoclear' : autoclear,
    'spam' : spamfilter,
    'joinmsg' : servermsg,
    'leavemsg' : servermsg,
    'todo' : todo,
    'todos' : todo,
    'ping' : ping,
    'restrict' : restrict,
    'timezone' : timezone,
    'tag' : tag,
    'ffs' : ffs,
    'log' : log,
    'timeit' : timeit,
    'link' : link,
    'unlink' : unlink
}

command_log = {
    'help' : 0,
    'info' : 0,
    'remind' : 0,
    'blacklist' : 0,
    'interval' : 0,
    'del' : 0,
    'donate' : 0,
    'clear' : 0,
    'autoclear' : 0,
    'spam' : 0,
    'joinmsg' : 0,
    'leavemsg' : 0,
    'todo' : 0,
    'todos' : 0,
    'ping' : 0,
    'restrict' : 0,
    'timezone' : 0,
    'tag' : 0,
    'ffs' : 0,
    'log' : 0,
    'timeit' : 0
}

try:
    with open('DATA/log.json', 'r') as f:
        command_log = json.load(f)
except FileNotFoundError:
    with open('DATA/log.json', 'w') as f:
        json.dump(command_log, f)

async def validate_cmd(message): ## method for doing the commands
    if message.guild != None and message.guild.id in prefix.keys():
        pref = prefix[message.guild.id]
    else:
        pref = '$'

    if message.content[0] != pref: ## These functions call if the prefix isnt present
        if message.content.startswith('mbprefix'):

            if message.channel.id in channel_blacklist:
                await blacklist_msg(message)
                return

            await change_prefix(message)
        return

    cmd = message.content.split(' ')[0][1:] # extract the keyword
    if cmd in command_map.keys():

        if message.channel.id in channel_blacklist and cmd not in ['help', 'blacklist']:
            await blacklist_msg(message)
            return

        else:
            try:
                command_log[cmd] += 1
            except KeyError:
                command_log[cmd] = 1

            await command_map[cmd](message, client)
            with open('DATA/log.json', 'w') as f:
                json.dump(command_log, f)
            return


async def watch_spam(message):
    if message.author.id in users.keys(): ## all the stuff to do with spam filtering
        if time.time() - users[message.author.id] < 2:

            if message.author.id in warnings.keys():

                warnings[message.author.id] += 1
                if warnings[message.author.id] == 4:
                    await message.channel.send('Please slow down {}'.format(message.author.mention))

                elif warnings[message.author.id] == 6:

                    await message.channel.set_permissions(message.author, send_messages=False)
                    await message.channel.send('{}, you\'ve been muted for spam. Please contact an admin to review your status.'.format(message.author.mention))

            else:
                print('user added to warning list')
                warnings[message.author.id] = 1

            users[message.author.id] = time.time()

        else:
            users[message.author.id] = time.time()
            warnings[message.author.id] = 0

    else:
        print('registered user for auto-muting')
        users[message.author.id] = time.time()

async def send():
    if not dbl_token:
        return

    session = aiohttp.ClientSession()
    dump = json.dumps({
        'server_count': len(client.guilds)
    })

    head = {
        'authorization': dbl_token,
        'content-type' : 'application/json'
    }

    url = 'https://discordbots.org/api/bots/stats'
    async with session.post(url, data=dump, headers=head) as resp:
        print('returned {0.status} for {1}'.format(resp, dump))

    session.close()

@client.event ## print some stuff to console when the bot is activated
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    await client.change_presence(activity=discord.Game(name='$info ¬ mbprefix <p>'))

    del_queue = []
    for channel in autoclears.keys():
        if client.get_channel(channel) == None:
            print('removed {}'.format(channel))
            del_queue.append(channel)

    for i in del_queue:
        del autoclears[i]

    del_queue = []

    for channel in channel_blacklist:
        if client.get_channel(channel) == None:
            print('removed {}'.format(channel))
            del_queue.append(channel)

    for i in del_queue:
        channel_blacklist.remove(i)

@client.event
async def on_guild_join(guild):
    await send()
    try:
        c = [channel for channel in guild.text_channels if channel.permissions_for(guild.get_member(client.user.id)).send_messages]
        await c[0].send(embed=discord.Embed(description='Thank you for adding me to your server! Use the command `$info` to get more information, and use the `$restrict` command (admin) to allow roles to set server reminders.'))
    except discord.errors.Forbidden:
        pass
    except IndexError:
        pass

@client.event
async def on_guild_remove(guild):
    await send()

@client.event
async def on_message(message): ## when a message arrives at the bot ##
    if time.time() - times['last_loop'] > 15:
        print('ERROR LOOP TAKING TOO LONG TO RUN')

    skip_command = False

    if message.author.id == client.user.id: ## if the message has been sent by the bot ##
        skip_command = True

    if message.content in ['', None]: ## if the message is a file ##
        skip_command = True

    try:
        if not skip_command:
            await validate_cmd(message)

        ## run stuff here if there is no command ##
        if message.channel.id in autoclears.keys(): ## autoclearing
            await asyncio.sleep(autoclears[message.channel.id])
            try:
                await message.delete()
            except discord.errors.NotFound:
                pass

        if message.channel.id in spam_filter:
            await watch_spam(message)

    except discord.errors.Forbidden:
        try:
            await message.channel.send(embed=discord.Embed(title='Failed to perform an action: Not enough permissions (403)'))
        except discord.errors.Forbidden:
            try:
                await message.channel.send('Failed to perform actions on {}: Not enough permissions (403)'.format(message.guild.name))
            except discord.errors.Forbidden:
                pass

@client.event
async def on_member_join(member):
    if member.guild.id in join_messages.keys():
        try:
            await client.get_channel(join_messages[member.guild.id][1]).send(join_messages[member.guild.id][0].format(member.name))
        except:
            print('Issue encountered administering member join message.')

@client.event
async def on_member_remove(member):
    if member.guild.id in leave_messages.keys():
        try:
            await client.get_channel(leave_messages[member.guild.id][1]).send(leave_messages[member.guild.id][0].format(member.name))
        except:
            print('Issue encountered administering member leave message.')

try:
    client.loop.create_task(check_reminders())

    coro = asyncio.start_server(server.handle_inbound, '0.0.0.0', 44139, loop=client.loop)
    server = client.loop.run_until_complete(coro)

    client.run(config.get('DEFAULT', 'token'))
except Exception as e:
    print('Error detected. Restarting in 15 seconds.')
    print(e)
    time.sleep(15)

    os.execl(sys.executable, sys.executable, *sys.argv)
