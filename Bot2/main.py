from server_data import ServerData
from sloccount import sloccount_py
from Reminder import Reminder

import discord
import msgpack
import pytz

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

        self.commands = {
            'help' : self.help,
            'info' : self.info,
            'donate' : self.donate,

            'prefix' : self.change_prefix,
            'blacklist' : self.blacklist,

            'timezone' : self.timezone,

            'remind' : self.remind,
            'interval' : self.interval,
            'delete' : self.delete,

            'todo' : self.todo,
            'tag' : self.tag,

            'autoclear' : self.autoclear,
            'clear' : self.clear,
        }

        self.strings = {
            'help' : 'NULL'
        }

        self.template = {
            'id' : 0,
            'prefix' : self.DEFAULT_PREFIX,
            'timezone' : 'UTC',
            'autoclears' : {},
            'blacklist' : [],
            'restrictions' : {}
        }

        try:
            with open('data.msgpack.zlib', 'rb') as f:
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

        connection = sqlite3.connect('DATA/calendar.db') #open SQL db
        cursor = connection.cursor() #place cursor
        cursor.row_factory = sqlite3.Row #set row to read as SQLite Rows

        cursor.execute('SELECT * FROM reminders') #select all rows
        for reminder in cursor.fetchall(): #for all rows...
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
            open('EXT/strings.py', 'r').close()
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

        if message.author.bot or message.content == None:
            return

        if message.guild is not None and len([d for d in self.data if d.id == message.guild.id]) == 0:
            s = ServerData(**self.template)
            s.id = message.guild.id

            self.data.append(s)

        with open('EXT/strings.py', 'r') as f:
            self.strings = eval(f.read())

        if await self.get_cmd(message):
            with open('data.msgpack.zlib', 'wb') as f:
                f.write(zlib.compress(msgpack.packb([d.__dict__ for d in self.data])))


    async def get_cmd(self, message):

        server = None if message.guild is None else self.get_server(message.guild)
        prefix = '$' if server is None else server.prefix

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
                if scope not in server.restrictions.keys():
                    server.restrictions[scope] = []
                for role in message.author.roles:
                    if role.id in server.restrictions[scope]:
                        break
                else:
                    await message.channel.send(embed=discord.Embed(description=self.strings['remind']['no_perms']))
                    return

        self.reminders.append(Reminder(time=msg_time, channel=scope, message=msg_text))
        self.reminders.sort(key=lambda x: x.time)

        await message.channel.send(embed=discord.Embed(description=self.strings['remind']['success'].format(pref, scope, round(msg_time - time.time()))))
        print('Registered a new reminder for {}'.format(message.guild.name))


    async def interval(self, message, stripped, server):
        pass


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
        pass


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
                if role.id not in server.restrictions[message.channel.id]:
                    disengage_all = False
                server.restrictions[message.channel.id].append(role.id)

            if disengage_all and args:
                for role in message.role_mentions:
                    server.restrictions[message.channel.id].remove(role.id)
                    server.restrictions[message.channel.id].remove(role.id)

                await message.channel.send(embed=discord.Embed(description=self.strings['restrict']['disabled']))

            elif args:
                await message.channel.send(embed=discord.Embed(description=self.strings['restrict']['enabled']))

            else:
                await message.channel.send(embed=discord.Embed(description=self.strings['restrict']['allowed'].format(' '.join(['<@&' + str(i) + '>' for i in server.restrictions[message.channel.id]]))))


    async def tag(self, message, stripped, server):
        pass


    async def todo(self, message, stripped, server):
        if 'todos' in message.content.split(' ')[0]:
            if isinstance(message.channel, discord.DMChannel):
                await message.channel.send('Please use `$todo` for your personal TODO list. `$todos` is only for server use.')
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
                msg.append('*Do `${0} add <message>` to add an item to your TODO, or type `${0} help` for more commands!*'.format(command))
            await message.channel.send(embed=discord.Embed(title='{}\'s TODO'.format(name), description=''.join(msg)))

        elif len(splits) >= 2:
            if splits[0] in ['add', 'a']:
                a = ' '.join(splits[1:])
                if len(a) > 80:
                    await message.channel.send('Sorry, but TODO message sizes are limited to 80 characters. Keep it concise :)')
                    return

                elif len(''.join(todo)) > 800:
                    await message.channel.send('Sorry, but TODO lists are capped at 800 characters. Maybe, get some things done?')
                    return

                self.todos[location].append(a)
                await message.channel.send('Added \'{}\' to todo!'.format(a))

            elif splits[0] in ['remove', 'r']:
                try:
                    a = self.todos[location].pop(int(splits[1])-1)
                    await message.channel.send('Removed \'{}\' from todo!'.format(a))

                except ValueError:
                    await message.channel.send('Removal item must be a number. View the numbered TODOs using `${}`'.format(command))
                except IndexError:
                    await message.channel.send('Couldn\'t find item by that number. Are you in the correct todo list?')

            elif splits[0] in ['remove*', 'r*', 'clear', 'clr']:
                self.todos[location] = []
                await message.channel.send('Cleared todo list!')

            else:
                await message.channel.send('To use the TODO commands, do `${0} add <message>`, `${0} remove <number>`, `${0} clear` and `${0}` to add to, remove from, clear or view your todo list.'.format(command))

        else:
            await message.channel.send('To use the TODO commands, do `${0} add <message>`, `${0} remove <number>`, `${0} clear` and `${0}` to add to, remove from, clear or view your todo list.'.format(command))

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

        await message.channel.send('Listing reminders on this server... (there may be a small delay, please wait for the "List (1,2,3...)" message)')

        n = 1
        remli = []

        for rem in self.reminders:
            if rem.channel in li:
                remli.append(rem)
                await message.channel.send('  **' + str(n) + '**: \'' + rem.message + '\' (' + datetime.datetime.fromtimestamp(rem.time, pytz.timezone('UTC' if server is None else server.timezone)).strftime('%Y-%m-%d %H:%M:%S') + ')')
                n += 1

        await message.channel.send('List (1,2,3...) the reminders you wish to delete, or type anything else to cancel.')

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

        await message.channel.send('Deleted {} reminders!'.format(dels))

client = BotClient()
client.run(client.config.get('DEFAULT', 'token'))
