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

            'timezone' : self.timezone
        }

        self.strings = {
            'help' : 'NULL'
        }

        self.template = {
            'id' : 0,
            'prefix' : self.DEFAULT_PREFIX,
            'timezone' : 'UTC',
            'autoclear' : {},
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

        config = configparser.SafeConfigParser()
        config.read('config.ini')
        self.dbl_token = config.get('DEFAULT', 'dbl_token')
        self.patreon = config.get('DEFAULT', 'patreon_enabled') == 'yes'
        self.patreonserver = int(config.get('DEFAULT', 'patreon_server'))

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
            open('strings.py', 'r').close()
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
                        date.replace(month=a[1], day=a[0])
                    elif len(a) == 3:
                        date.replace(year=a[2], month=a[1], day=a[0])

                elif ':' in clump:
                    a = clump.split(':')
                    if len(a) == 2:
                        date.replace(hour=a[0], minute=a[1])
                    elif len(a) == 3:
                        date.replace(hour=a[0], minute=a[1], second=a[2])
                    else:
                        return None

                else:
                    date.replace(day=clump)

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

        if isinstance(message.channel, discord.DMChannel) or message.author.bot or message.content == None:
            return

        if len([d for d in self.data if d.id == message.guild.id]) == 0:
            s = ServerData(**self.template)
            s.id = message.guild.id

            self.data.append(s)

        with open('strings.py', 'r') as f:
            self.strings = eval(f.read())

        if await self.get_cmd(message):
            with open('data.msgpack.zlib', 'wb') as f:
                f.write(zlib.compress(msgpack.packb([d.__dict__ for d in self.data])))


    async def get_cmd(self, message):

        server = self.get_server(message.guild)
        prefix = server.prefix

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
                    await message.channel.send(embed=discord.Embed(description='Please ensure your tag links directly to a user or channel, not a role.'))
                    return

            if args[0][1] == '@': # if the scope is a user
                pref = '@'
                scope = message.guild.get_member(tag)

            else:
                pref = '#'
                scope = message.guild.get_channel(tag)

            if scope is None:
                await message.channel.send(embed=discord.Embed(description='Couldn\'t find a location by your tag present.'))
                return

            else:
                scope = scope.id

            args.pop(0)

        msg_time = format_time(args[0], server)

        if msg_time is None:
            await message.channel.send(embed=discord.Embed(description='Make sure the time you have provided is in the format of [num][s/m/h/d][num][s/m/h/d] etc. or `day/month/year-hour:minute:second`.'))
            return

        args.pop(0)

        msg_text = ' '.join(args)

        if self.count_reminders(scope) > 5 and message.author not in self.get_patrons('Patrons'):
            await message.channel.send(embed=discord.Embed(description='Too many reminders in specified channel! Use `$del` to delete some of them, or use `$donate` to increase your maximum ($5 tier)'))
            return

        if len(msg_text) > 150 and message.author not in self.get_patrons('Patrons'):
            await message.channel.send(embed=discord.Embed(description='Reminder message too long! (max 150, you used {}). Use `$donate` to increase your character limit to 1900 ($5 tier)'.format(len(msg_text))))
            return

        if len(msg_text) >= 1900:
            await message.channel.send(embed=discord.Embed(description='Discord restrictions mean we can\'t send reminders 2000+ characters. Sorry'))
            return

        if pref == '#':
            if not message.author.guild_permissions.manage_messages:
                if scope not in server.restrictions.keys():
                    server.restrictions[scope] = []
                for role in message.author.roles:
                    if role.id in server.restrictions[scope]:
                        break
                else:
                    await message.channel.send(embed=discord.Embed(description='You must be either admin or have a role capable of sending reminders to that channel. Please talk to your server admin, and tell her/him to use the `$restrict` command to specify allowed roles.'))
                    return

        self.reminders.append(Reminder(time=msg_time, channel=scope, message=msg_text))
        self.reminders.sort(key=lambda x: x.time)

        await message.channel.send(embed=discord.Embed(description='New reminder registered for <{}{}> in {} seconds . You can\'t edit the reminder now, so you are free to delete the message.'.format(pref, scope, round(msg_time - time.time()))))
        print('Registered a new reminder for {}'.format(message.guild.name))


    async def interval(self, message, stripped, server):


    async def autoclear(self, message, stripped, server):


    async def blacklist(self, message, stripped, server):


    async def clear(self, message, stripped, server):
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


    async def todo(self, message, stripped, server):


    async def delete(self, message, stripped, server):



try: ## token grabbing code
    with open('token','r') as token_f:
        token = token_f.read().strip('\n')

except:
    print('no token provided')
    sys.exit(-1)

client = BotClient()
client.run(client.config.get('DEFAULT', 'token'))
