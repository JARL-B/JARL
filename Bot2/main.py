from server_data import ServerData
from sloccount import sloccount_py
from Reminder import Reminder

import discord
import msgpack
import pytz
import asyncio

from itertools import chain
import zlib
import datetime
import time
import sys
import os
import configparser
import sqlite3
import json

class BotClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super(BotClient, self).__init__(*args, **kwargs)
        self.get_server = lambda x: [d for d in self.data if d.id == x.id][0]

        self.data = []
        self.reminders = []
        self.DEFAULT_PREFIX = '$'

        self.times = {
            'last_loop' : time.time(),
            'start' : 0,
            'loops' : 0
        }

        self.commands = {
            'help' : self.help,
            'info' : self.info,
            'donate' : self.donate,

            'prefix' : self.change_prefix,
            'blacklist' : self.blacklist,
            'restrict' : self.restrict,

            'timezone' : self.timezone,
            'lang' : self.language,

            'remind' : self.remind,
            'interval' : self.interval,
            'del' : self.delete,

            'todo' : self.todo,
            'todos' : self.todo,
            'tag' : self.tag,

            'autoclear' : self.autoclear,
            'clear' : self.clear,
        }

        self.strings = {
            'help' : 'NULL'
        }

        self.languages = {
            'english' : 'EN',
            'spanish' : 'ES'
        }

        self.template = {
            'id' : 0,
            'prefix' : self.DEFAULT_PREFIX,
            'timezone' : 'UTC',
            'autoclears' : {},
            'blacklist' : [],
            'restrictions' : [],
            'tags' : {},
            'language' : 'EN'
        }

        try:
            with open('DATA/data.msgpack.zlib', 'rb') as f:
                for d in msgpack.unpackb(zlib.decompress(f.read()), encoding='utf8'):
                    self.validate_data(d)
                    self.data.append(ServerData(**d))
        except FileNotFoundError:
            pass

        self.config = configparser.SafeConfigParser()
        self.config.read('config.ini')
        self.dbl_token = self.config.get('DEFAULT', 'dbl_token')
        self.patreon = self.config.get('DEFAULT', 'patreon_enabled') == 'yes'
        self.patreonserver = int(self.config.get('DEFAULT', 'patreon_server'))

        if self.patreon:
            print('Patreon is enabled. Will look for server {}'.format(patreonserver))

        self.reminders = []

        self.connection = sqlite3.connect('DATA/calendar.db') #open SQL db
        self.cursor = self.connection.cursor() #place cursor
        self.cursor.execute('''PRAGMA journal_mode=DELETE;''')
        self.cursor.row_factory = sqlite3.Row #set row to read as SQLite Rows

        self.cursor.execute('SELECT * FROM reminders') #select all rows
        for reminder in self.cursor.fetchall(): #for all rows...
            self.reminders.append(Reminder(dictv=dict(reminder))) #place each in the list

        self.reminders.sort(key=lambda x: x.time)

        try:
            with open('DATA/todos.json', 'r') as f:
                self.todos = json.load(f)
                self.todos = {int(x) : y for x, y in self.todos.items()}
        except FileNotFoundError:
            print('No todos file found')
            self.todos = {}

        try:
            with open('DATA/process_deletes.mp', 'rb') as f:
                self.process_deletes = msgpack.unpack(f, encoding='utf8')
        except FileNotFoundError:
            print('No deletes file found')
            self.process_deletes = {}

        try:
            open('EXT/strings_EN.py', 'r').close()
        except FileNotFoundError:
            print('Strings file not present. Exiting...')
            sys.exit()


    def validate_data(self, d):
        for key, default in self.template.items():
            if key not in d.keys():
                d[key] = default


    def count_reminders(self, loc):
        return len([r for r in self.reminders if r.channel == loc and r.interval == None])


    def get_patrons(self, level='Patrons'):
        if self.patreon:
            p_server = client.get_guild(self.patreonserver)
            p_role = discord.utils.get(p_server.roles, name=level)
            premiums = [user for user in p_server.members if p_role in user.roles]

            return premiums
        else:
            return client.get_all_members()

    def format_time(self, text, server):
        if '/' in text or ':' in text:
            date = datetime.datetime.now(pytz.timezone(server.timezone))

            for clump in text.split('-'):
                if '/' in clump:
                    a = clump.split('/')
                    if len(a) == 2:
                        date = date.replace(month=int(a[1]), day=int(a[0]))
                    elif len(a) == 3:
                        date = date.replace(year=int(a[2]), month=int(a[1]), day=int(a[0]))

                elif ':' in clump:
                    a = clump.split(':')
                    if len(a) == 2:
                        date = date.replace(hour=int(a[0]), minute=int(a[1]))
                    elif len(a) == 3:
                        date = date.replace(hour=int(a[0]), minute=int(a[1]), second=int(a[2]))
                    else:
                        return None

                else:
                    date = date.replace(day=int(clump))

            return date.timestamp()

        else:
            current_buffer = '0'
            seconds = 0
            minutes = 0
            hours = 0
            days = 0

            for char in text:

                if char == 's':
                    seconds = int(current_buffer)
                    current_buffer = '0'

                elif char == 'm':
                    minutes = int(current_buffer)
                    current_buffer = '0'

                elif char == 'h':
                    hours = int(current_buffer)
                    current_buffer = '0'

                elif char == 'd':
                    days = int(current_buffer)
                    current_buffer = '0'

                else:
                    try:
                        int(char)
                        current_buffer += char
                    except ValueError:
                        return None

            time_sec = round(time.time() + seconds + (minutes * 60) + (hours * 3600) + (days * 86400) + int(current_buffer))
            return time_sec


    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------------')
        await client.change_presence(activity=discord.Game(name='@{} help'.format(self.user.name)))


    async def on_guild_remove(self, guild):
        self.data = [d for d in self.data if d.id != guild.id]


    async def on_message(self, message):
        if message.guild is not None and len([d for d in self.data if d.id == message.guild.id]) == 0:
            s = ServerData(**{
                'id' : 0,
                'prefix' : self.DEFAULT_PREFIX,
                'timezone' : 'UTC',
                'autoclears' : {},
                'blacklist' : [],
                'restrictions' : [],
                'tags' : {},
                'language' : 'EN'
            })
            s.id = message.guild.id

            self.data.append(s)

        server = None if message.guild is None else self.get_server(message.guild)
        if server is not None and message.channel.id in server.autoclears.keys():
            self.process_deletes[message.id] = {'time' : time.time() + server.autoclears[message.channel.id], 'channel' : message.channel.id}

        if message.author.bot or message.content == None:
            return

        with open('EXT/strings_{}.py'.format('EN' if server is None else server.language), 'r') as f:
            self.strings = eval(f.read())

        if await self.get_cmd(message):
            with open('DATA/data.msgpack.zlib', 'wb') as f:
                f.write(zlib.compress(msgpack.packb([d.__dict__ for d in self.data])))


    async def get_cmd(self, message):

        server = None if message.guild is None else self.get_server(message.guild)
        prefix = '$' if server is None else server.prefix

        if message.content.startswith('mbprefix'):
            await self.change_prefix(message, ' '.join(message.content.split(' ')[1:]), server)


        if server is None or message.channel.id not in server.blacklist or message.content.startswith(('{}help'.format(server.prefix), '{}blacklist'.format(server.prefix))):
            if message.content[0:len(prefix)] == prefix:
                command = (message.content + ' ')[len(prefix):message.content.find(' ')]
                if command in self.commands:
                    stripped = (message.content + ' ')[message.content.find(' '):].strip()
                    await self.commands[command](message, stripped, server)
                    return True

            elif self.user.id in map(lambda x: x.id, message.mentions) and len(message.content.split(' ')) > 1:
                if message.content.split(' ')[1] in self.commands.keys():
                    stripped = (message.content + ' ').split(' ', 2)[-1].strip()
                    await self.commands[message.content.split(' ')[1]](message, stripped, server)
                    return True

        else:
            await message.channel.send(embed=discord.Embed(description=self.strings['blacklisted']))

        return False


    async def change_prefix(self, message, stripped, server):
        if server is None:
            return

        if stripped:
            stripped += ' '
            server.prefix = stripped[:stripped.find(' ')]
            await message.channel.send(self.strings['prefix']['success'].format(prefix=server.prefix))

        else:
            await message.channel.send(self.strings['prefix']['no_argument'].format(prefix=server.prefix))


    async def help(self, message, *args):
        embed = discord.Embed(description=self.strings['help'])
        await message.channel.send(embed=embed)


    async def info(self, message, stripped, server):
        embed = discord.Embed(description=self.strings['info'].format(prefix=server.prefix, sloc=sloccount_py(), user=self.user.name))
        await message.channel.send(embed=embed)


    async def donate(self, message, stripped, server):
        embed = discord.Embed(description=self.strings['donate'])
        await message.channel.send(embed=embed)


    async def timezone(self, message, stripped, server):
        if server is None:
            return

        if stripped == '':
            await message.channel.send(embed=discord.Embed(description=self.strings['timezone']['no_argument'].format(prefix=server.prefix, timezone=server.timezone)))

        else:
            if stripped not in pytz.all_timezones:
                await message.channel.send(embed=discord.Embed(description=self.strings['timezone']['no_timezone']))
            else:
                server.timezone = stripped
                d = datetime.datetime.now(pytz.timezone(server.timezone))

                await message.channel.send(embed=discord.Embed(description=self.strings['timezone']['success'].format(timezone=server.timezone, time=d.strftime('%H:%M:%S'))))


    async def language(self, message, stripped, server):
        if server is None:
            return

        if stripped.lower() in self.languages.keys():
            server.language = self.languages[stripped.lower()]

        elif stripped.upper() in self.languages.values():
            server.language = stripped.upper()

        else:
            await message.channel.send(embed=discord.Embed(description=self.strings['lang']['invalid']))

    async def remind(self, message, stripped, server):
        if server is None:
            return

        args = stripped.split(' ')

        if len(args) < 2:
            await message.channel.send(embed=discord.Embed(description=self.strings['remind']['no_argument']))
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
                    await message.channel.send(embed=discord.Embed(description=self.strings['remind']['invalid_tag']))
                    return

            if args[0][1] == '@': # if the scope is a user
                pref = '@'
                scope = message.guild.get_member(tag)

            else:
                pref = '#'
                scope = message.guild.get_channel(tag)

            if scope is None:
                await message.channel.send(embed=discord.Embed(description=self.strings['remind']['invalid_tag']))
                return

            else:
                scope = scope.id

            args.pop(0)

        try:
            msg_time = self.format_time(args[0], server)
        except ValueError:
            await message.channel.send(embed=discord.Embed(description=self.strings['remind']['invalid_time']))
            return

        if msg_time is None:
            await message.channel.send(embed=discord.Embed(description=self.strings['remind']['invalid_time']))
            return

        args.pop(0)

        msg_text = ' '.join(args)

        if self.count_reminders(scope) > 5 and message.author not in self.get_patrons('Patrons'):
            await message.channel.send(embed=discord.Embed(description=self.strings['remind']['invalid_count']))
            return

        if len(msg_text) > 150 and message.author not in self.get_patrons('Patrons'):
            await message.channel.send(embed=discord.Embed(description=self.strings['remind']['invalid_chars'].format(len(msg_text))))
            return

        if len(msg_text) >= 1900:
            await message.channel.send(embed=discord.Embed(description=self.strings['remind']['invalid_chars_2000']))
            return

        if pref == '#':
            if not message.author.guild_permissions.manage_messages:
                for role in message.author.roles:
                    if role.id in server.restrictions:
                        break
                else:
                    await message.channel.send(embed=discord.Embed(description=self.strings['remind']['no_perms']))
                    return

        self.reminders.append(Reminder(time=msg_time, channel=scope, message=msg_text))
        self.reminders.sort(key=lambda x: x.time)

        await message.channel.send(embed=discord.Embed(description=self.strings['remind']['success'].format(pref, scope, round(msg_time - time.time()))))
        print('Registered a new reminder for {}'.format(message.guild.name))


    async def interval(self, message, stripped, server):
        if server is None:
            return

        if message.author not in self.get_patrons('Donor'):
            await message.channel.send(embed=discord.Embed(description=self.strings['interval']['donor']))
            return

        args = message.content.split(' ')
        args.pop(0) # remove the command item

        if len(args) < 3:
            await message.channel.send(embed=discord.Embed(description=self.strings['interval']['no_argument']))
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
                    await message.channel.send(embed=discord.Embed(description=self.strings['remind']['invalid_tag']))

            if args[0][1] == '@': # if the scope is a user
                pref = '@'
                scope = message.guild.get_member(tag)

            else:
                pref = '#'
                scope = message.guild.get_channel(tag)

            if scope is None:
                await message.channel.send(embed=discord.Embed(description=self.strings['remind']['invalid_tag']))
                return

            else:
                scope = scope.id

            args.pop(0)

        msg_time = self.format_time(args[0], message.guild.id)

        if msg_time == None:
            await message.channel.send(embed=discord.Embed(description=self.strings['remind']['invalid_time']))
            return

        args.pop(0)

        msg_interval = self.format_time(args[0], message.guild.id)

        if msg_interval == None:
            await message.channel.send(embed=discord.Embed(description=self.strings['interval']['invalid_interval']))
            return

        msg_interval -= time.time()
        msg_interval = round(msg_interval)

        if msg_interval < 8:
            await message.channel.send(embed=discord.Embed(description=self.strings['interval']['8_seconds']))
            return

        args.pop(0)

        msg_text = ' '.join(args)

        if len(msg_text) > 150 and message.author not in self.get_patrons('Patrons'):
            await message.channel.send(embed=discord.Embed(description=self.strings['remind']['invalid_chars'].format(len(msg_text))))
            return

        if len(msg_text) >= 1900:
            await message.channel.send(embed=discord.Embed(description=self.strings['remind']['invalid_chars_2000']))
            return

        if pref == '#':
            if not message.author.guild_permissions.manage_messages:
                for role in message.author.roles:
                    if role.id in server.restrictions:
                        break
                else:
                    await message.channel.send(embed=discord.Embed(description=self.strings['remind']['no_perms']))
                    return

        self.reminders.append(Reminder(time=msg_time, interval=msg_interval, channel=scope, message=msg_text))
        self.reminders.sort(key=lambda x: x.time)

        await message.channel.send(embed=discord.Embed(description=self.strings['interval']['success'].format(pref, scope, round(msg_time - time.time()))))
        print('Registered a new interval for {}'.format(message.guild.name))


    async def autoclear(self, message, stripped, server):
        if server is None:
            return

        if not message.author.guild_permissions.administrator:
            await message.channel.send(embed=discord.Embed(description=self.strings['admin_required']))
            return

        seconds = 10

        for item in stripped.split(' '): # determin a seconds argument
            try:
                seconds = float(item)
                break
            except ValueError:
                continue

        if len(message.channel_mentions) == 0:
            if message.channel.id in server.autoclears.keys():
                del server.autoclears[message.channel.id]
                await message.channel.send(embed=discord.Embed(description=self.strings['autoclear']['disable'].format(message.channel.mention)))
            else:
                server.autoclears[message.channel.id] = seconds
                await message.channel.send(embed=discord.Embed(description=self.strings['autoclear']['enable'].format(seconds, message.channel.mention)))

        else:
            disable_all = True
            for i in message.channel_mentions:
                if i.id not in server.autoclears.keys():
                    disable_all = False
                server.autoclears[i.id] = seconds


            if disable_all:
                for i in message.channel_mentions:
                    del server.autoclears[i.id]

                await message.channel.send(embed=discord.Embed(description=self.strings['autoclear']['disable'].format(', '.join(map(lambda x: x.name, message.channel_mentions)))))
            else:
                await message.channel.send(embed=discord.Embed(description=self.strings['autoclear']['enable'].format(seconds)))


    async def blacklist(self, message, stripped, server):
        if server is None:
            return

        if not message.author.guild_permissions.administrator:
            await message.channel.send(embed=discord.Embed(description=self.strings['admin_required']))
            return

        if len(message.channel_mentions) > 0:
            disengage_all = True

            for mention in message.channel_mentions:
                if mention.id not in server.blacklist:
                    disengage_all = False

            if disengage_all:
                for mention in message.channel_mentions:
                    server.blacklist.remove(mention.id)

                await message.channel.send(embed=discord.Embed(description=self.strings['blacklist']['removed_from']))

            else:
                for mention in message.channel_mentions:
                    if mention.id not in server.blacklist:
                        server.blacklist.append(mention.id)

                await message.channel.send(embed=discord.Embed(description=self.strings['blacklist']['added_from']))

        else:
            if message.channel.id in server.blacklist:
                server.blacklist.remove(message.channel.id)
                await message.channel.send(embed=discord.Embed(description=self.strings['blacklist']['removed']))

            else:
                server.blacklist.append(message.channel.id)
                await message.channel.send(embed=discord.Embed(description=self.strings['blacklist']['added']))



    async def clear(self, message, stripped, server):
        if server is None:
            return

        if not message.author.guild_permissions.administrator:
            await message.channel.send(embed=discord.Embed(description=self.strings['admin_required']))
            return

        if len(message.mentions) == 0:
            await message.channel.send(embed=discord.Embed(description=self.strings['clear']['no_argument']))
            return

        delete_list = []

        async for m in message.channel.history(limit=1000):
            if time.time() - m.created_at.timestamp() >= 1209600 or len(delete_list) > 99:
                break

            if m.author in message.mentions:
                delete_list.append(m)

        await message.channel.delete_messages(delete_list)


    async def restrict(self, message, stripped, server):
        if server is None:
            return

        if not message.author.guild_permissions.administrator:
            await message.channel.send(embed=discord.Embed(description=self.strings['admin_required']))

        else:
            disengage_all = True
            args = False

            for role in message.role_mentions:
                args = True
                if role.id not in server.restrictions:
                    disengage_all = False
                server.restrictions.append(role.id)

            if disengage_all and args:
                for role in message.role_mentions:
                    server.restrictions.remove(role.id)
                    server.restrictions.remove(role.id)

                await message.channel.send(embed=discord.Embed(description=self.strings['restrict']['disabled']))

            elif args:
                await message.channel.send(embed=discord.Embed(description=self.strings['restrict']['enabled']))

            else:
                await message.channel.send(embed=discord.Embed(description=self.strings['restrict']['allowed'].format(' '.join(['<@&' + str(i) + '>' for i in server.restrictions]))))


    async def tag(self, message, stripped, server):
        if server is None:
            return

        not_done = True

        splits = stripped.split(' ')

        if stripped == '':
            if len(server.tags) == 0:
                await message.channel.send(embed=discord.Embed(title='No Tags!', description=self.strings['tags']['help']))
            else:
                await message.channel.send(embed=discord.Embed(title='Tags', description='\n'.join(server.tags.keys())))

            not_done = False

        elif len(splits) > 1:
            content = ' '.join(splits[1:])

            if splits[0] in ['add', 'new']:
                if len(server.tags) > 5 and message.author not in self.get_patrons('Patrons'):
                    await message.channel.send(self.strings['tags']['invalid_count'])
                    return

                elif len(content) > 80 and message.author not in self.get_patrons('Patrons'):
                    await message.channel.send(self.strings['tags']['invalid_chars'])
                    return

                content = content.split(':')
                if len(content) == 1:
                    await message.channel.send(self.strings['tags']['colon'])

                else:
                    if content[0].startswith(('add', 'new', 'remove', 'del')):
                        await message.channel.send(self.strings['tags']['illegal'])
                        return

                    server.tags[content[0]] = ':'.join(content[1:]).strip()
                    await message.channel.send(self.strings['tags']['added'].format(content[0]))

                not_done = False

            elif splits[0] in ['remove', 'del']:
                name = ' '.join(splits[2:])
                if name not in server.tags.keys():
                    await message.channel.send(self.strings['tags']['unfound'])
                    return

                del server.tags[name]
                await message.channel.send(self.strings['tags']['deleted'].format(name))

                not_done = False

        if not_done:
            name = ' '.join(splits).strip()

            if name not in server.tags.keys():
                await message.channel.send(self.strings['tags']['help'])
                return

            await message.channel.send(server.tags[name])


    async def todo(self, message, stripped, server):
        if 'todos' in message.content.split(' ')[0]:
            if server is None:
                await message.channel.send(self.strings['todo']['server_only'])
                return

            location = message.guild.id
            name = message.guild.name
            command = 'todos'
        else:
            location = message.author.id
            name = message.author.name
            command = 'todo'


        if location not in self.todos.keys():
            self.todos[location] = []

        splits = stripped.split(' ')

        todo = self.todos[location]

        if len(splits) == 1:
            msg = ['\n{}: {}'.format(i+1, todo[i]) for i in range(len(todo))]
            if len(msg) == 0:
                msg.append(self.strings['todo']['add'].format(prefix='$' if server is None else server.prefix, command=command))
            await message.channel.send(embed=discord.Embed(title='{}\'s TODO'.format(name), description=''.join(msg)))

        elif len(splits) >= 2:
            if splits[0] in ['add', 'a']:
                a = ' '.join(splits[1:])
                if len(a) > 80:
                    await message.channel.send(self.strings['todo']['too_long'])
                    return

                elif len(''.join(todo)) > 800:
                    await message.channel.send(self.strings['todo']['too_long2'])
                    return

                self.todos[location].append(a)
                await message.channel.send(self.strings['todo']['added'].format(name=a))

            elif splits[0] in ['remove', 'r']:
                try:
                    a = self.todos[location].pop(int(splits[1])-1)
                    await message.channel.send(self.strings['todo']['removed'].format(a))

                except ValueError:
                    await message.channel.send(self.strings['todo']['error_value'].format(prefix='$' if server is None else server.prefix, command=command))
                except IndexError:
                    await message.channel.send(self.strings['todo']['error_index'])

            elif splits[0] in ['remove*', 'r*', 'clear', 'clr']:
                self.todos[location] = []
                await message.channel.send(self.strings['todo']['cleared'])

            else:
                await message.channel.send(self.strings['todo']['help'].format(prefix='$' if server is None else server.prefix, command=command))

        else:
            await message.channel.send(self.strings['todo']['help'].format(prefix='$' if server is None else server.prefix, command=command))

        with open('DATA/todos.json', 'w') as f:
            json.dump(self.todos, f)


    async def delete(self, message, stripped, server):
        if server is not None:
            if not message.author.guild_permissions.manage_messages:
                scope = message.channel.id
                if scope not in restrictions.keys():
                    server.restrictions[scope] = []
                for role in message.author.roles:
                    if role.id in server.restrictions[scope]:
                        break
                else:
                    await message.channel.send(embed=discord.Embed(description=self.strings['remind']['no_perms']))
                    return

            li = [ch.id for ch in message.guild.channels] ## get all channels and their ids in the current server
        else:
            li = [message.author.id]

        await message.channel.send(self.strings['del']['listing'])

        n = 1
        remli = []

        for rem in self.reminders:
            if rem.channel in li:
                remli.append(rem)
                await message.channel.send('  **' + str(n) + '**: \'' + rem.message + '\' (' + datetime.datetime.fromtimestamp(rem.time, pytz.timezone('UTC' if server is None else server.timezone)).strftime('%Y-%m-%d %H:%M:%S') + ')')
                n += 1

        await message.channel.send(self.strings['del']['listed'])

        num = await client.wait_for('message', check=lambda m: m.author == message.author and m.channel == message.channel)
        nums = [n.strip() for n in num.content.split(',')]

        dels = 0
        for i in nums:
            try:
                i = int(i) - 1
                if i < 0:
                    continue
                self.reminders.remove(remli[i])
                print('Deleted reminder')
                dels += 1

            except ValueError:
                continue
            except IndexError:
                continue

        await message.channel.send(self.strings['del']['count'].format(dels))


    async def check_reminders(self):
        await self.wait_until_ready()

        self.times['start'] = time.time()
        while not self.is_closed():
            self.times['last_loop'] = time.time()
            self.times['loops'] += 1

            while len(self.reminders) and self.reminders[0].time <= time.time():
                print('Looping for reminder(s)...')

                reminder = self.reminders.pop(0)

                if reminder.interval is not None and reminder.interval < 8:
                    continue

                users = self.get_all_members()
                channels = self.get_all_channels()

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
                        patrons = self.get_patrons('Donor')

                        if any([m in patrons for m in server_members]):
                            if reminder.message.startswith('-del_on_send'):
                                try:
                                    await recipient.purge(check=lambda m: m.content == reminder.message[len('-del_on_send'):].strip() and time.time() - m.created_at.timestamp() < 1209600 and m.author == client.user)
                                except Exception as e:
                                    print(e)

                                await recipient.send(reminder.message[len('-del_on_send'):])

                            elif reminder.message.startswith('-del_after_'):

                                chars = ''

                                for char in reminder.message[len('-del_after_'):]:
                                    if char in '0123456789':
                                        chars += char
                                    else:
                                        break

                                wait_time = int(chars)

                                message = await recipient.send(reminder.message[len('-del_after_{}'.format(chars)):])

                                self.process_deletes[message.id] = {'time' : time.time() + wait_time, 'channel' : message.channel.id}

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
                            await recipient.send(self.strings['interval']['removed'])
                            continue

                        while reminder.time <= time.time():
                            reminder.time += reminder.interval ## change the time for the next interval

                        self.reminders.append(reminder) # Requeue the interval with modified time
                        self.reminders.sort(key=lambda x: x.time)

                except Exception as e:
                    print(e)

            self.cursor.execute('DELETE FROM reminders')
            self.cursor.execute('VACUUM')

            for d in map(lambda x: x.__dict__, self.reminders):

                command = '''INSERT INTO reminders (interval, time, channel, message)
                VALUES (?, ?, ?, ?)'''

                self.cursor.execute(command, (d['interval'], d['time'], d['channel'], d['message']))

            self.connection.commit()

            try:
                for message, info in self.process_deletes.copy().items():
                    if info['time'] <= time.time():
                        del self.process_deletes[message]

                        message = await self.get_channel(info['channel']).get_message(message)

                        if message is None or message.pinned:
                            pass
                        else:
                            print('{}: Attempting to auto-delete a message...'.format(datetime.datetime.utcnow().strftime('%H:%M:%S')))
                            try:
                                await message.delete()
                            except Exception as e:
                                print(e)

            except Exception as e:
                print('Error in deletion loop: {}'.format(e))

            with open('DATA/process_deletes.mp', 'wb') as f:
                msgpack.dump(self.process_deletes, f)

            await asyncio.sleep(2.5)

client = BotClient()

try:
    client.loop.create_task(client.check_reminders())

    client.run(client.config.get('DEFAULT', 'token'))
except Exception as e:
    print('Error detected. Restarting in 15 seconds.')
    print(sys.exc_info()[0])
    time.sleep(15)

    os.execl(sys.executable, sys.executable, *sys.argv)
